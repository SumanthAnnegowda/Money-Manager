from django.shortcuts import render
from .serializers import UserRegistrationSerializer, LoginSerializer, LogoutSerializer
from .models import get_token_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from .utils import TOKEN_TTL, TOKEN_PREFIX
from django.utils import timezone
from rest_framework import serializers


class RegisterUser(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        username = request.data["username"]
        User = get_user_model()
        user = None
        email_exists = User.objects.filter(email = username).exists()
        if email_exists:
            user = User.objects.get(email=username)
        _, token = get_token_model().objects.create(
            user=user, expiry=TOKEN_TTL, prefix=TOKEN_PREFIX
        )

        expiry = timezone.now() + TOKEN_TTL

        return Response(
            {
                'username': username,
                'token': str(token),
                'expiry': int(expiry.timestamp() * 1000),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_superuser,
            },
            status=status.HTTP_201_CREATED)


class Logout(APIView):
    def post(self, request, format=None):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

