from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import get_token_model

# Register your models here.
admin.site.register(get_user_model())
admin.site.register(get_token_model())
