from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from .serializers import UserSerializer, EmailVerificationSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import status 
from dashboard.models import User, Email_Verification, Password_Reset_Request
from django.db import IntegrityError
import random
from django.core.mail import EmailMessage
import threading
from .email_controller import send_mail
import imaplib2

# Create your views here.
class EmailThread(threading.Thread):
    """
    Email Thread Class:
    This is to speed the process of sending email to users
    The thread will be used so as to not use network thread
    """

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        """
        Execute the message
        """
        self.email.send(fail_silently=False)


class LoginApiView(APIView):

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')

        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            # user = authenticated_user
            # subject = 'PayAboki Account Activation'
            # body = 'Hello ' + user.username + ', Please use the code below to verify your account.\n'+str(6768689)+'\n' + '\n' + '\n'+'Thankyou for choosing PayAboki'
            

            # send_mail(
            #     subject,
            #     body,
            #     "najibkado@gmail.com",
            # )

            # EmailThread(new_email).start()

            serializer = UserSerializer(authenticated_user)
            token = Token.objects.get(user=authenticated_user).key
            return Response({ 'user_id': authenticated_user.id, 'user':serializer.data ,'token': token }, status=status.HTTP_200_OK)

            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRegisterApiView(APIView):

    # def get(self, request):
    #     users = User.objects.all()
    #     serializer = UserSerializer(users, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            token = Token.objects.create(user=user)
            try:
                otp = Email_Verification(
                    user = user,
                    code = str(random.randint(100000, 999999))
                )
                otp.save()
                print(otp.code)
                #TODO: Send Email Verification Code to user
                 #Send User Email Verification Mail
                subject = 'PayAboki Account Activation'
                body = 'Hello ' + user.username + ', Please use the code below to verify your account.\n'+ '\n' + otp.code + '\n' + '\n' + '\n'+'Thankyou for choosing PayAboki'
                sender_email = 'payaboki00@gmail.com'
                
                send_mail(
                    subject,
                    body,
                    user.email,
                )

            except IntegrityError:
                pass
            return Response({'user_id': user.id, 'user': serializer.data, 'token': token.key }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class EmailApiVerificationView(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = User.objects.get(pk=id)
        try:
            otp = Email_Verification(
                user = user,
                code = str(random.randint(100000, 999999))
            )
            otp.save()
            print(otp.code)

            subject = 'PayAboki Account Activation'
            body = 'Hello ' + user.username + ', Please use the code below to verify your account.\n'+ '\n' + otp.code+'\n' + '\n' + '\n'+'Thankyou for choosing PayAboki'
            sender_email = 'payaboki00@gmail.com'
            
            send_mail(
                subject,
                body,
                user.email,
            )

        except IntegrityError:
            return Response(status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def post(self, request, id):
        serializer = EmailVerificationSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(pk=int(serializer.data['user']))
            otp = Email_Verification.objects.filter(user=user).last()
            if int(otp.code) == int(serializer.data['code']):
                user.is_verified = True
                user.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordRecoveryAPIView(APIView):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            print(user)
        except User.DoesNotExist:
            print("Hello World!")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            otp = Email_Verification(
                user = user,
                code = str(random.randint(100000, 999999))
            )
            otp.save()

            print(otp.code)

            subject = 'PayAboki Account Recovery'
            body = 'Hello ' + user.username + ', Please use the code below to recover your password.\n'+ '\n' + otp.code+'\n' + '\n' + '\n'+'Thankyou for choosing PayAboki'
            sender_email = 'payaboki00@gmail.com'
            
            send_mail(
                subject,
                body,
                user.email,
            )
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def post(self, request, username):
        data=request.data
        try:
            user = User.objects.get(username=data['user'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        otp = Email_Verification.objects.filter(user=user).last()
        if int(otp.code) == int(data['code']):
            reset_req = Password_Reset_Request(
                user = user,
                is_verified = True,
                has_set_new = False
            )
            reset_req.save() 
            print(otp.code)
            return Response({"reset_link" : f"https://payaboki.com/api/reset/new/{reset_req.pk}"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class PasswordResetAPIView(APIView):

    def post(self, request, id):
        data = request.data
        try:
            req = Password_Reset_Request.objects.get(pk=id)
        except Password_Reset_Request.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if req.has_set_new:
            return Response(status=status.HTTP_208_ALREADY_REPORTED)

        user = req.user

        user.set_password(data['new_password'])
        req.has_set_new = True
        req.save()
        user.save()
        subject = 'PayAboki Account Recovery'
        body = 'Hello ' + user.username + '\n' + '\n' +',Your password has been successfully reset.\n'+ '\n' + "If you didn't initiate this request, Please be sure to go and reset your password immediately." +'\n' + '\n' + '\n'+'Thankyou for choosing PayAboki'
        
        send_mail(
            subject,
            body,
            user.email,
        )
        return Response(status=status.HTTP_202_ACCEPTED)

        
        