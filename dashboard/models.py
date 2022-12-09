from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)

class Landing_Logs(models.Model):
    landing_page = models.IntegerField()
    
class application_Logs(models.Model):
    application_page = models.IntegerField()

class unique_Logs(models.Model):
    unique = models.IntegerField()
    
class Email_Verification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)