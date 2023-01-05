from django.contrib import admin
from .models import Transaction, Escrow

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Escrow)
