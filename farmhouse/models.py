# bookings/models.py
from django.db import models
from django.contrib.auth.models import User

class Farm(models.Model):

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField()
    available_to = models.DateField()

    def __str__(self):
        return self.name

class FarmImage(models.Model):
    farm = models.ForeignKey(Farm, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='farm_images/')

    def __str__(self):
        return f"Image for {self.farm.name}"


class Booking(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('farm', 'check_in', 'check_out')

    def __str__(self):
        return f"Booking for {self.farm.name} by {self.user.username}"
