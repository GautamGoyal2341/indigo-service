from django.db import models
from flights.models_helper import FlightStatusChoices

class Airline(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Gate(models.Model):
    gate_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.gate_number

class Flight(models.Model):
    flight_id = models.CharField(max_length=10, unique=True)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=FlightStatusChoices.choices)  
    departure_gate = models.ForeignKey(Gate, related_name='departure_flights', on_delete=models.CASCADE)
    arrival_gate = models.ForeignKey(Gate, related_name='arrival_flights', on_delete=models.CASCADE)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    actual_departure = models.DateTimeField(null=True, blank=True)
    actual_arrival = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.flight_id
    

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

class Notification(models.Model):
    flight_details = models.TextField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)