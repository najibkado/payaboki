from django.contrib import admin
from .models import Transaction, Escrow, Wallet, User

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Escrow)
admin.site.register(Wallet)
admin.site.register(User)
