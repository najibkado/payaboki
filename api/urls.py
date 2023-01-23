from django.urls import path
from . import views

urlpatterns = [
    path('logout', views.LogoutApiView.as_view()),
    path('login', views.LoginApiView.as_view()),
    path('register', views.UserRegisterApiView.as_view()),
    path('verify/<int:id>', views.EmailApiVerificationView.as_view()),
    path('recover/<str:username>', views.PasswordRecoveryAPIView.as_view()),
    path('reset/new/<int:id>', views.PasswordResetAPIView.as_view()),
    path('send', views.TransactionsAPIView.as_view()),
    path('escrow', views.EscrowAPIView.as_view()),
    path('escrow/approve/<int:id>', views.ApproveEscrowAPIView.as_view()),
    path('user-data', views.UserDataUpdateAPIView.as_view()),
    path('user/<str:username>', views.GetUserInfoAPIView.as_view()),
]