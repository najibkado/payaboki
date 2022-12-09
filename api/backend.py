import jwt 
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User
from main.models import Developer

class JWTAuth(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None
        
        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            code = payload['code']
            if int(code) == 1:
                user = User.objects.get(username=payload['username'])
                return (user, token)
            elif int(code) == 2:
                developer = Developer.objects.get(api_key=payload['api_key'])
                return (developer.wallet.user, token)
            
        except jwt.DecodeError as e:
            raise exceptions.AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed('Expired Token')

        return super().authenticate(request)