import datetime
import time
import jwt
from django.conf import settings
def generate_tokens(user):
    access_token_payload = {
        'user_id': user.username,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=0, minutes=3),
        'iat': int(time.time()),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')

    refresh_token_payload = {
        'user_id': user.username,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7),
        'iat': int(time.time()),
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return {'access': access_token, 'refresh': refresh_token}
