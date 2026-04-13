from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password',
                  )

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Emmmmail',
            'password': 'Password',
        }

        help_texts = {
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'email': 'The e-mail must be valid',
        }

        error_messages = {
            'username': {
                'required': 'Username is required.',
            },
            'email': {
                'invalid': 'Please enter a valid email address.',
                'required': 'Email is required.',
            },
            'password': {
                'required': 'Password is required.',
            },
        }

        widgets = {
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here',
            }),
        }