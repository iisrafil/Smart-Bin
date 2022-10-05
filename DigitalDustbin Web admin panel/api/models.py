from django.db import models
from datetime import datetime


class AppUser(models.Model):
    id = models.CharField(primary_key=True, max_length=14)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class Device(models.Model):
    user = models.ForeignKey(AppUser, related_name='devices', on_delete=models.CASCADE, blank=True, null=True)
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=80)
    location = models.TextField()
    dustbinHeight = models.IntegerField()
    percentage = models.IntegerField(null=True, blank=True)
    gas = models.FloatField(null=True, blank=True)
    temp = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    status = models.BooleanField(default=True)
    lastFullTime = models.DateTimeField(null=True, blank=True)
    lastCleanTime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.pk


class Data(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now)
    height = models.FloatField()
    percent = models.IntegerField(blank=True, null=True)
    gas = models.FloatField()
    unwanted_gas = models.BooleanField(default=False)
    temp = models.FloatField()
    humidity = models.FloatField()

    def __str__(self):
        return "data on "+str(self.time)+" of device "+self.device.id