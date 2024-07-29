from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, NotificationAPIView, Subscribe

router = DefaultRouter()
router.register(r'flights', FlightViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('notifications/', NotificationAPIView.as_view(), name='notifications'),
    path('subscribe/', Subscribe.as_view(), name='subscribe_user'),

]
