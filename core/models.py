from django.contrib.auth.models import User
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=7, decimal_places=5)
    longitude = models.DecimalField(max_digits=7, decimal_places=5)

    def __str__(self):
        return self.name

class UserCity(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cities', null=True)
    count = models.PositiveIntegerField(default=0)
