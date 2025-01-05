from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .Manager import CustomUserManager

# Create your models here.


# User model

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    
    objects = CustomUserManager()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    def __str__(self):
        return self.email
    
    

# Post Model


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='post')
    created_at = models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return self.title