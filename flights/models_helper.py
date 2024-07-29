from django.db import models

class FlightStatusChoices(models.TextChoices):  
    SCHEDULED = 'scheduled', 'Scheduled'  
    ON_TIME = 'on_time', 'On Time'  
    DELAYED = 'delayed', 'Delayed'  
    CANCELED = 'canceled', 'Canceled'  
    BOARDING = 'boarding', 'Boarding'  
    IN_AIR = 'in_air', 'In Air'  
    LANDED = 'landed', 'Landed'  