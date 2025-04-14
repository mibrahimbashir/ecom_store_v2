from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from storefront.models import UserProfile


class ShippingAddress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                             blank=True, null=True)

    full_name = models.CharField(max_length=40)
    phone_number = PhoneNumberField(region='PK')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32, blank=True, null=True)
    postal_code = models.CharField(max_length=16)

    def __str__(self):
        return f'Shipping Address {self.id}'
