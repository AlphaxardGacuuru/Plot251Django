from django.db import models

# Create your models here.


class WaterReadings(models.Model):
    apartment = models.CharField(max_length=200)
    reading = models.IntegerField(default=0)
    created_at = models.DateTimeField("date published")

    def __str__(self):
        return self.apartment


class WaterPayments(models.Model):
    apartment = models.ForeignKey(WaterReadings, on_delete=models.CASCADE)
    payment = models.IntegerField(default=0)
    created_at = models.DateTimeField("date published")

    def __str__(self):
        return self.apartment.apartment
