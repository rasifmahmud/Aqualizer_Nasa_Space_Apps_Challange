from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Task(models.Model):
    completed = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    description = models.TextField()

class WaterParticle(models.Model):    
    deviceID = models.CharField(max_length=50)   
    user = models.CharField(max_length=50,null = True)
    ph = models.FloatField(blank=True,null = True,default=0)
    temperature = models.FloatField(blank=True,null = True,default=0)
    orp = models.FloatField(blank=True,null = True,default=0)
    salinity=models.FloatField(blank=True,null = True,default=0)
    dateTime = models.DateTimeField(blank=True,null = True)
    geoLocation = models.CharField(max_length=254,blank=True,null = True)
    token = models.CharField(max_length=254,blank=True,null= True)
    access = models.CharField(max_length=20,blank=True,null = True,default='public')

    def __unicode__(self):
        return self.deviceID

class Standard(models.Model):
    user= models.CharField(max_length=50)
    from_ph=models.FloatField(blank=True,null=True,default=0)
    to_ph=models.FloatField(blank=True,null=True,default=0)
    from_temperature=models.FloatField(blank=True,null=True,default=0)
    to_temperature=models.FloatField(blank=True,null=True,default=0)
    from_orp=models.FloatField(blank=True,null=True,default=0)
    to_orp=models.FloatField(blank=True,null=True,default=0)
    from_salinity=models.FloatField(blank=True,null=True,default=0)
    to_salinity=models.FloatField(blank=True,null=True,default=0)


class UserDevice(models.Model):
    user = models.CharField(max_length=50)
    deviceID = models.CharField(max_length=50)
    mobileNo = models.CharField(max_length=25,blank=True,null= True)
    access = models.CharField(max_length=20,blank=True,null = True)

    def __unicode__(self):
        return self.deviceID

