from datetime import datetime, timedelta

import jwt
from django.conf import settings
# from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError
from .models import User
from rest_framework import exceptions
from rest_framework.response import Response
class SafeJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None  # No 'Authorization' header, so return None

        try:
            # Split the 'Authorization' header to get the token
            token_prefix, access_token = authorization_header.split(' ')
            
            # Make sure the token prefix is 'Bearer'
            if token_prefix != 'Bearer':
                raise exceptions.AuthenticationFailed('Invalid token prefix')

            # Decode the JWT token
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            print("TGVFDFVGHYUHBFEFVDCV")
            print(access_token)
            raise exceptions.AuthenticationFailed('Access token expired')
        except (ValueError, jwt.DecodeError):
            print("tune mera dil lutya")
            print(access_token)
            raise exceptions.AuthenticationFailed('Invalid token')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        # Find the user based on the token payload
        user = User.objects.filter(username=payload['user_id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        # Return the authenticated user and token
        return (user, access_token)
