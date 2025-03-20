from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    phone_number = PhoneNumberField(region='PK', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    state = models.CharField(max_length=32, blank=True, null=True)
    postal_code = models.CharField(max_length=16, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_profile_pics/', blank=True, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email