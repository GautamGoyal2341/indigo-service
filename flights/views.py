from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Flight, User
from .serializers import FlightSerializer, UserSubscriptionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer
import pika
import json

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'departure_gate__gate_number', 'arrival_gate__gate_number']
    search_fields = ['flight_id', 'airline__name']
    ordering_fields = ['scheduled_departure', 'scheduled_arrival']


class NotificationAPIView(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Add notification to RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='notifications')
            message = json.dumps(serializer.data)
            channel.basic_publish(exchange='',
                                  routing_key='notifications',
                                  body=message)
            connection.close()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Subscribe(APIView):
    def post(self, request):
        serializer = UserSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            user, created = User.objects.get_or_create(name=name, defaults={'email': email})
            if not created:
                return Response({'detail': 'User with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'User subscribed successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
