from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    empty_value_display = '-Empty-'
    search_fields = ['email', 'phone_number']
    list_display = ['email', 'username', 'phone_number', 'date_joined']
    fieldsets = [
        ('Email & Username', {'fields': ['email', 'username']}),
        ('Cart', {'fields': ['cart']}),
        ('Personal Info', {'fields': ['first_name', 'last_name', 'phone_number']}),
        ('Shipping Info', {'fields': ['address', ('city', 'state'), 'postal_code']}),
    ]

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'username', 'password1', 'password2'),
            },
        ),
    )
