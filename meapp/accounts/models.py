from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from django.core.validators import EmailValidator
from accounts.helpers import validators as v
import datetime as dt



class CalculatorAccessRole(models.Model):
    walls = models.BooleanField(default=False)
    windows = models.BooleanField(default=False)
    roof = models.BooleanField(default=False)
    occupants = models.BooleanField(default=False)
    equipments = models.BooleanField(default=False)
    role_name = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Calculator Access Roles'
        ordering = ['role_name']
        unique_together = ('walls', 'windows', 'roof', 'occupants', 'equipments')
    def __str__(self):
        return self.role_name


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
    calc_access = models.ForeignKey(CalculatorAccessRole, on_delete=models.PROTECT, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name']

    def __str__(self):
        return f'{self.email} : {self.first_name}'