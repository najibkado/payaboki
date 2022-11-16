from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashhome'),
    path('conversions/', views.conversions, name="dashconversions"),
    path('login/', views.index, name='dashindex'),
    
]