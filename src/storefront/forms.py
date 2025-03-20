from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class CustomerForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Choose a strong password at \
              least 8 characters long.'
        self.fields['password2'].help_text = ''