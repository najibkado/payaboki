from django.db import models

# Create your models here.
class EarlyAccess(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    fee = models.CharField(max_length=255)
    news = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)