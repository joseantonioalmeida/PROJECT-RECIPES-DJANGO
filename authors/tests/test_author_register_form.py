from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex: John'),
        ('last_name', 'Ex: Doe'),
        ('username', 'Ex: johndoe'),
        ('email', 'Ex: johndoe@example.com'),
        ('password', 'You password'),
        ('password2', 'Repeat your password')
    ])
    def test_field_placeholders_are_correct(self, field_name, expected_placeholder):
        form = RegisterForm()
        placeholder = form[field_name].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, expected_placeholder)