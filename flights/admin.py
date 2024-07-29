# flights/admin.py
from django.contrib import admin
from .models import Flight, Airline, Gate, Notification, User

class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_id', 'airline', 'status', 'departure_gate', 'arrival_gate', 'scheduled_departure', 'scheduled_arrival', 'actual_departure', 'actual_arrival')
    list_filter = ('status', 'airline')
    search_fields = ('flight_id', 'airline__name')

class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class GateAdmin(admin.ModelAdmin):
    list_display = ('gate_number',)
    search_fields = ('gate_number',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('status',)

# Register the models with the custom admin classes
admin.site.register(Flight, FlightAdmin)
admin.site.register(Airline, AirlineAdmin)
admin.site.register(Gate, GateAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(User, UserAdmin)
