from django.db import models
import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('شماره موبایل الزامی است.')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password or self.make_random_password())
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('male', 'آقا'),
        ('female', 'خانم'),
        ('other', 'سایر...'),
    ]
    ROLE_CHOICES = (
        ('customer', 'کاربر مشتری'),
        ('owner', 'کاربر مدیر رستوران'),
        ('admin', 'کاربر مدیر'),
    )

    phone = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.full_name or self.phone} - {self.role}'


class OTP(models.Model):
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def is_invalid(self):
        return timezone.now() < self.created_at + timedelta(minutes=2)

    def __str__(self):
        return f'{self.phone} - {self.code} ({"done" if self.verified else "failed"})'

