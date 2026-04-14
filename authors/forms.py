import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            'Password must have at least one uppercase letter,'
            'one lowercase letter, and one digit. The length should be'
            'at least 8 characters ',
            code='invalid'
        )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Ex: John')
        add_placeholder(self.fields['last_name'], 'Ex: Doe')
        add_placeholder(self.fields['username'], 'Ex: johndoe')
        add_placeholder(self.fields['email'], 'Ex: johndoe@example.com')
        add_placeholder(self.fields['password'], 'You password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[strong_password],
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(),
    )
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password',
                  )

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email',
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

    def clean(self):
        cleaned_data = super().clean() 
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_cofirmation_error = ValidationError(
            'Password and password confirmation do not match.',
            code='invalid'
        )
            raise ValidationError({
                'password': password_cofirmation_error,
                'password2':[
                    password_cofirmation_error,
                    ValidationError('Please confirm your password.', code='required')
                ],
            })