from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser
from .utils import TOKEN_PREFIX, TOKEN_TTL, TOKEN_KEY_LENGTH, MAXIMUM_TOKEN_PREFIX_LENGTH, DIGEST_LENGTH, create_token_string, hash_token
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.apps  import apps


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=230)
    last_name = models.CharField(max_length=230)
    created_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = CustomUserManager()


class AuthTokenManager(models.Manager):
    def create(
        self,
        user,
        expiry=TOKEN_TTL,
        prefix=TOKEN_PREFIX
    ):
        token = prefix + create_token_string()
        digest = hash_token(token)
        if expiry is not None:
            expiry = timezone.now() + expiry
        instance = super(AuthTokenManager, self).create(
            token_key=token[:TOKEN_KEY_LENGTH], digest=digest,
            user=user, expiry=expiry)
        return instance, token
    

class AbstractAuthToken(models.Model):

    objects = AuthTokenManager()

    digest = models.CharField(
        max_length=DIGEST_LENGTH, primary_key=True)
    token_key = models.CharField(
        max_length=MAXIMUM_TOKEN_PREFIX_LENGTH +
        TOKEN_KEY_LENGTH,
        db_index=True
    )
    user = models.ForeignKey(CustomUser, null=False, blank=False,
                             related_name='auth_token_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()

    class Meta:
        abstract = True

    def __str__(self):
        return '%s : %s' % (self.digest, self.user)


class AuthToken(AbstractAuthToken):
    class Meta:
        swappable = 'TOKEN_MODEL'


def get_token_model():
    """
    Return the AuthToken model that is active in this project.
    """

    try:
        return apps.get_model(settings.TOKEN_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "TOKEN_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "TOKEN_MODEL refers to model '%s' that has not been installed"
            % settings.TOKEN_MODEL
        )
    