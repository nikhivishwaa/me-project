from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from django.core.validators import EmailValidator
from accounts.helpers import validators as v
import datetime as dt


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, validators=[EmailValidator, v.validate_email])
    phone_number = models.CharField(max_length=10, unique=True, validators=[v.validate_phone_number])
    first_name = models.CharField(max_length=150, validators=[v.validate_first_name])
    last_name = models.CharField(max_length=150, blank=True, validators=[v.validate_last_name])
    verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6,blank=True, null=True)
    otp_timestamp = models.DateTimeField(auto_now_add=True)
    is_restricted = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name']

    def __str__(self):
        return f'{self.email} : {self.first_name}'
