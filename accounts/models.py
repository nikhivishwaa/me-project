from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
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
    


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is Required')

        if not phone_number:
            raise ValueError('Phone Number is Required')

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('calc_access', CalculatorAccessRole.objects.get(role_name='allowAll'))

        return self.create_user(email, phone_number, password=password,**extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, validators=[EmailValidator, v.validate_email])
    phone_number = models.CharField(max_length=10, unique=True, validators=[v.validate_phone_number])
    first_name = models.CharField(max_length=150, validators=[v.validate_first_name])
    last_name = models.CharField(max_length=150, blank=True, validators=[v.validate_last_name])
    verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6,blank=True, null=True)
    forgot_password_otp = models.CharField(max_length=6, null=True, blank=True)
    password_update_token = models.CharField(max_length=100, null=True, blank=True)
    otp_timestamp = models.DateTimeField(auto_now_add=True)
    forgot_otp_timestamp = models.DateTimeField(blank=True, null=True)
    is_restricted = models.BooleanField(default=True)
    calc_access = models.ForeignKey(CalculatorAccessRole, on_delete=models.PROTECT, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name']

    def __str__(self):
        return f'{self.email} : {self.first_name}'
    

def create_roles():
    roles = [
        {'walls': True, 'windows': True, 'roof': True, 'occupants': True, 'equipments': True, 'role_name': 'allowAll'},
        {'walls': False, 'windows': False, 'roof': False, 'occupants': False, 'equipments': True, 'role_name': 'allowEquipments'},
        {'walls': False, 'windows': False, 'roof': False, 'occupants': True, 'equipments': False, 'role_name': 'allowOccupants'},
        {'walls': False, 'windows': False, 'roof': True, 'occupants': False, 'equipments': False, 'role_name': 'allowRoof'},
        {'walls': True, 'windows': True, 'roof': True, 'occupants': False, 'equipments': False, 'role_name': 'allowRoom'},
        {'walls': True, 'windows': False, 'roof': False, 'occupants': False, 'equipments': False, 'role_name': 'allowWalls'},
        {'walls': True, 'windows': True, 'roof': False, 'occupants': False, 'equipments': False, 'role_name': 'allowWallsAndWindows'},
        {'walls': False, 'windows': True, 'roof': False, 'occupants': False, 'equipments': False, 'role_name': 'allowWindows'},
        {'walls': False, 'windows': False, 'roof': False, 'occupants': False, 'equipments': False, 'role_name': 'denyAll'},
    ]


    for i in roles:
        try:
            CalculatorAccessRole.objects.get_or_create(**i)
        except Exception as e:
            print("failed to create:", i['role_name'])

    else:
        print("roles initialized")
