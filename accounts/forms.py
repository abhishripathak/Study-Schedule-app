from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optional: Add placeholders and basic styling
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password',
        })
