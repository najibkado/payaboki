from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from .serializers import UserSerializer, EmailVerificationSerializer, TransactionSerializer, EscrowSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import status 
from dashboard.models import User, Email_Verification, Password_Reset_Request, Wallet, Transaction, Escrow, DepositRequest
from django.db import IntegrityError
import random
from django.core.mail import EmailMessage
import threading
from .email_controller import send_mail
import imaplib2
from decimal import Decimal
from . import payment_channel

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

            try:
                wallet = Wallet.objects.get(user=authenticated_user)
            except Wallet.DoesNotExist:
                wallet = Wallet(
                    user= authenticated_user,
                    balance = 0.00
                )

                wallet.save()
            

            serializer = UserSerializer(authenticated_user)
            token = Token.objects.get(user=authenticated_user).key
            escrow = []
            transactions = []

            esc = Escrow.objects.filter(sender = authenticated_user)
            esc2 = Escrow.objects.filter(reciever = authenticated_user)
            tran = Transaction.objects.filter(sender = authenticated_user)
            tran2 = Transaction.objects.filter(reciever = authenticated_user)

            for i in esc:
                escrow.append(i.to_json())

            for i in esc2:
                escrow.append(i.to_json())

            for i in tran:
                transactions.append(i.to_json())

            for i in tran2:
                transactions.append(i.to_json())

            wallet = Wallet.objects.get(user=authenticated_user)



            data = {
                "user": { 'user_id': authenticated_user.id, 'user':serializer.data ,'token': token },
                "profile": { 'username': serializer.data["username"], 'name': serializer.data["first_name"], 'phone': serializer.data["last_name"] },
                "escrowInfo": { 'trans': escrow },
                "transactions": transactions,
                "walletInfo": { 'wallet_id': wallet.user.username, 'balance': wallet.balance}
            }
            return Response(data, status=status.HTTP_200_OK)

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

            try:
                wallet = Wallet(
                    user= user,
                    balance = 0.00
                )

                wallet.save()
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

class TransactionsAPIView(APIView):
    #TODO: Remove SessionAuth
    #TODO: Implement Emails and Charges 
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():
            sender = serializer.validated_data['sender']
            reciever = serializer.validated_data['reciever']

            sender_wallet = Wallet.objects.get(user=sender)
            reciever_wallet = Wallet.objects.get(user=reciever)

            if Decimal(sender_wallet.balance) > Decimal(serializer.validated_data['amount']):
                balance = Decimal(sender_wallet.balance) - Decimal(serializer.validated_data['amount'])
                sender_wallet.balance = balance
                sender_wallet.save()

                rcv_balance = Decimal(reciever_wallet.balance) + Decimal(serializer.validated_data['amount'])
                reciever_wallet.balance = rcv_balance
                reciever_wallet.save()
            else:
                return Response({"error":"Insufficient Balance"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EscrowAPIView(APIView):
    #TODO: Remove SessionAuth
    #TODO: Implement Emails and Charges 
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EscrowSerializer(data=request.data)
        if serializer.is_valid():
            sender = serializer.validated_data['sender']

            sender_wallet = Wallet.objects.get(user=sender)

            if Decimal(sender_wallet.balance) > Decimal(serializer.validated_data['amount']):
                serializer.save()
            else:
                return Response({"error":"Insufficient Balance"}, status=status.HTTP_400_BAD_REQUEST)
   
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApproveEscrowAPIView(APIView):
    #TODO: Remove SessionAuth
    #TODO: Implement Emails
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        escrow = Escrow.objects.get(pk=id)

        if escrow.sender == request.user:
            sender = escrow.sender
            reciever = escrow.reciever

            sender_wallet = Wallet.objects.get(user=sender)
            reciever_wallet = Wallet.objects.get(user=reciever)

            balance = Decimal(sender_wallet.balance) - Decimal(escrow.amount)
            sender_wallet.balance = balance
            sender_wallet.save()

            rcv_balance = Decimal(reciever_wallet.balance) + Decimal(escrow.amount)
            reciever_wallet.balance = rcv_balance
            reciever_wallet.save()

            escrow.is_approved = True
            escrow.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDataUpdateAPIView(APIView):
    #TODO: Remove SessionAuth
    # authentication_classes = [SessionAuthentication, TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        authenticated_user =User.objects.get(pk=3)
        # try:
        #     wallet = Wallet.objects.get(user=authenticated_user)
        # except Wallet.DoesNotExist:
        #     wallet = Wallet(
        #         user= authenticated_user,
        #         balance = 10000.00
        #     )
        #     wallet.save()
        

        serializer = UserSerializer(authenticated_user)
        escrow = []
        transactions = []

        esc = Escrow.objects.filter(sender = authenticated_user)
        esc2 = Escrow.objects.filter(reciever = authenticated_user)
        tran = Transaction.objects.filter(sender = authenticated_user)
        tran2 = Transaction.objects.filter(reciever = authenticated_user)

        for i in esc:
            escrow.append(i.to_json())

        for i in esc2:
            escrow.append(i.to_json())

        for i in tran:
            transactions.append(i.to_json())

        for i in tran2:
            transactions.append(i.to_json())

        wallet = Wallet.objects.get(user=authenticated_user)



        data = {
            "user": { 'user_id': authenticated_user.id, 'user':serializer.data},
            "profile": { 'username': serializer.data["username"], 'name': serializer.data["first_name"], 'phone': serializer.data["last_name"] },
            "escrowInfo": { 'trans': escrow },
            "transactions": transactions,
            "walletInfo": { 'wallet_id': wallet.user.username, 'balance': wallet.balance}
        }
        return Response(data, status=status.HTTP_200_OK)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserInfoAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "Unable to get user"})

        return Response({"user": user.first_name, "id": user.pk}, status=status.HTTP_200_OK)


class GetVirtualAccount(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, amount):
        deposit_req = DepositRequest(user=request.user)
        deposit_req.save()
        flw = payment_channel.FlutterwavePaymentCollector()
        acct = flw.create_virtual_account(request.user.first_name, request.user.email, str(deposit_req.ref), amount)

        return Response(acct, status=status.HTTP_200_OK)


    
    