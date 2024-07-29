from rest_framework import serializers
from .models import Flight, Airline, Gate, Notification, User

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'

class GateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gate
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    airline = AirlineSerializer()
    departure_gate = GateSerializer()
    arrival_gate = GateSerializer()

    class Meta:
        model = Flight
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['flight_details', 'status']

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']
