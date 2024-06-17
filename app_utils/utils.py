from users.models import CustomUser
from rest_framework.authtoken.models import Token

def getUserFromToken(request)->CustomUser:
    token = request.META.get('HTTP_AUTHORIZATION')
    token_string = token.split(' ')[-1]
    return Token.objects.get(key=token_string).user