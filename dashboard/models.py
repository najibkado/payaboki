from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass


class Landing_Logs(models.Model):
    landing_page = models.IntegerField()
    
class application_Logs(models.Model):
    application_page = models.IntegerField()

class unique_Logs(models.Model):
    unique = models.IntegerField()
    