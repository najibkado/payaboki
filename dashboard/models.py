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

class Password_Reset_Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=True)
    has_set_new = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=255 ,decimal_places=3)
    date = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usr_sender")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usr_reciever")
    amount = models.DecimalField(max_digits=255 ,decimal_places=3)
    method = models.IntegerField()
    datte = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    def to_json(self):
        return {
            "transaction_id": self.pk,
            "sender": self.sender.first_name,
            "reciever": self.reciever.first_name,
            "amount": self.amount,
            "method": self.method,
            "date": self.datte,
            "time": self.time
        }

class Escrow(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="escrow_usr_sender")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="escrow_usr_reciever")
    amount = models.DecimalField(max_digits=255 ,decimal_places=3)
    method = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    datte = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    def to_json(self):
        return {
            "escrow_id": self.pk,
            "sender": self.sender.first_name,
            "reciever": self.reciever.first_name,
            "amount": self.amount,
            "approved": self.is_approved,
            "method": self.method,
            "date": self.datte,
            "time": self.time
        }
    
