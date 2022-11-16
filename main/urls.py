from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('success', views.success, name="success"),
    path('error', views.error, name="error"),
    path('form', views.form, name="form"),
    path('seed', views.seed, name="seed")
]