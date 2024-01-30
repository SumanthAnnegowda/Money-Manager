from rest_framework import serializers
from django.contrib.auth import get_user_model
from .validations import validate_username, username_exists
from .models import *
import uuid
from datetime import timedelta
from django.utils import timezone
from .utils import TOKEN_TTL, TOKEN_PREFIX
from django.conf import settings


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

    def create(self, validated_data):
        email = validated_data["email"]
        User = get_user_model()

        user = User.objects.filter(email=email).first()
        if user != None:
            user.delete()
            user = None

        user = User.objects.create(
            email=email,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        user.set_password(validated_data["password"])
        user.save()

        return user
 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True, max_length=500)

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]

        is_valid_username, is_email = validate_username(username)
        if not is_valid_username:
            raise serializers.ValidationError("Invalid email")

        exists, is_email = username_exists(username=username, check_verified=False)
        if not exists:
            raise serializers.ValidationError("given username doesn't exist")
        exists, _ = username_exists(username=username)

        User = get_user_model()
        if is_email:
            user = User.objects.filter(email=username)[0]
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")

        return user


class LogoutSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    token = serializers.CharField(max_length=1000, write_only=True)

    def create(self, validated_data):
        username = validated_data['username']
        input_token = validated_data["token"]
        is_valid_username, _ = validate_username(username)
        if not is_valid_username:
            raise serializers.ValidationError("invalid username")
        
        exists, is_email = username_exists(username=username, check_verified=False)
        if not exists:
            raise serializers.ValidationError("username doesn't exist")

        if is_email:
            user = get_user_model().objects.get(email=username)
        try:
            token = get_token_model().objects.get(token_key=input_token)
            token.delete()
        except get_token_model().DoesNotExist:
            return user
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'first_name', 'last_name']
