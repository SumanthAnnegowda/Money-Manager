from .utils import validate_email
from django.contrib.auth import get_user_model

# Returns is_valid_username, is_email bool flags
def validate_username(username):
    if validate_email(username):
        return True, True
    return False, False

def username_exists(username, check_verified=True):
    User = get_user_model()
    if User.objects.filter(email=username).exists():
        return True, True
    return False, False