from django.contrib import admin
from .models import Transaction, Escrow, Wallet

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Escrow)
admin.site.register(Wallet)
