from django.contrib.auth.models import BaseUserManager


class  CustomUserManager(BaseUserManager):
    def create_user(self,  email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Call create_user method to handle password setting and user creation
        return self.create_user(email, password, **extra_fields)