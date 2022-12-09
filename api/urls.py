from django.urls import path
from . import views

urlpatterns = [
    path('logout', views.LogoutApiView.as_view()),
    path('login', views.LoginApiView.as_view()),
    path('register', views.UserRegisterApiView.as_view()),
    path('verify/<int:id>', views.EmailApiVerificationView.as_view()),
]