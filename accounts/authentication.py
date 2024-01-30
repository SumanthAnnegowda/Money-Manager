from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from .models import get_token_model
from django.utils import timezone

class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION') # get the token request header
        if not token: # no username passed in request headers
            return None # authentication did not succeed

        Token = get_token_model()
        try:
            stored_token = Token.objects.get(token_key=token) # get the user
            if stored_token.expiry < timezone.now():
                raise exceptions.AuthenticationFailed('Token expired')
            if stored_token is not None:
                user = stored_token.user
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        return (user, None) # authentication successful