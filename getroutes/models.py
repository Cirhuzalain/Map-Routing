from django.db import models

class LocationPrice(models.Model):
    truck_stop_id = models.IntegerField()
    truck_stop_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=5)
    rack_id = models.IntegerField()
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        indexes = [
            models.Index(fields=["truck_stop_name"]),
            models.Index(fields=["address"]),
            models.Index(fields=["city"]),
            models.Index(fields=["state"]),
        ]

class LocationRoute(models.Model):
    start_location = models.CharField(max_length=60)
    end_location = models.CharField(max_length=60)

    class Meta:
        indexes = [
            models.Index(fields=["start_location"]),
            models.Index(fields=["end_location"]),
        ]

class Routes(models.Model):
    distance = models.IntegerField()
    start_location_latlng = models.CharField(max_length=60)
    end_location_latlng = models.CharField(max_length=60)
    maneuver = models.CharField(max_length=60)
    instructions = models.CharField(max_length=300)
    travelMode = models.CharField(max_length=30)
    location_route = models.ForeignKey(LocationRoute, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["maneuver"]),
            models.Index(fields=["travelMode"]),
        ]
