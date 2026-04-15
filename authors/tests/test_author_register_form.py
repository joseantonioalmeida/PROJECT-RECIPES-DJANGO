from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse



class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex: John'),
        ('last_name', 'Ex: Doe'),
        ('username', 'Ex: johndoe'),
        ('email', 'Ex: johndoe@example.com'),
        ('password', 'You password'),
        ('password2', 'Repeat your password')
    ])
    def test_fields_placeholders_are_correct(self, field_name, expected_placeholder):
        form = RegisterForm()
        placeholder = form[field_name].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, expected_placeholder)
    
    @parameterized.expand([
        ('username', ('Username must have letters, numbers or one of those @/./+/-/_. '
            'The length should be between 4 and 150 characters.')),
        ('first_name', 'Enter your first name'),
        ('last_name', 'Enter your last name'),
        ('email', 'The e-mail must be valid'),
        ('password', 'Enter your password'),
        ('password2', 'Confirm your password.')
    ])
    def test_fields_help_text(self, field_name, expected_help_text):
        form = RegisterForm()
        help_text = form[field_name].field.help_text
        self.assertEqual(help_text, expected_help_text)


    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('username', 'Username'),
        ('email', 'Email'),
        ('password', 'Password'),
        ('password2', 'Confirm Password')
    ])
    def test_fields_labels(self, field_name, expected_label):
        form = RegisterForm()
        label = form[field_name].field.label
        self.assertEqual(label, expected_label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'user@example.com',
            'password': 'Str0ngp@ssword1',
            'password2': 'Str0ngp@ssword1'
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'Write your username.'),
        ('first_name', 'Write your first name.'),
        ('last_name', 'Write your last name.'),
        ('password', 'Password is required.'),
        ('password2', 'Confirm your password.'),
        ('email', 'E-mail is required.'),

    ])
    def test_fields_connot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        reponse = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, reponse.content.decode('utf-8'))
        self.assertIn(msg, reponse.context['form'].errors.get(field))

    
    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'usr'
        url = reverse('authors:create')
        reponse = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have at least 4 characters.'
        self.assertIn(msg, reponse.content.decode('utf-8'))
        self.assertIn(msg, reponse.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'u' * 151
        url = reverse('authors:create')
        reponse = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have less than 150 characters.'
        self.assertIn(msg, reponse.content.decode('utf-8'))
        self.assertIn(msg, reponse.context['form'].errors.get('username'))


    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        reponse = self.client.post(url, data=self.form_data, follow=True)
       
        msg = ('Password must have at least one uppercase letter,'
        'one lowercase letter, and one digit. The length should be'
        'at least 8 characters ')
       
        self.assertIn(msg, reponse.content.decode('utf-8'))
        self.assertIn(msg, reponse.context['form'].errors.get('password'))

        self.form_data['password'] = 'a@@bc123456'
        url = reverse('authors:create')
        reponse = self.client.post(url, data=self.form_data, follow=True)

        msg += 'Password and password confirmation do not match.'

        self.assertNotIn(msg, reponse.context['form'].errors.get('password'))

    
    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = 'Str0ngp@ssword1'
        self.form_data['password2'] = 'Str0ngp@ssword2'
        url = reverse('authors:create')
        reponse = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Password and password confirmation do not match.'
        self.assertIn(msg, reponse.content.decode('utf-8'))
        self.assertIn(msg, reponse.context['form'].errors.get('password'))
        
        self.form_data['password'] = 'Str0ngp@ssword'
        self.form_data['password2'] = 'Str0ngp@ssword'
        url = reverse('authors:create')
        reponse = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Password and password confirmation do not match.'
        self.assertNotIn(msg, reponse.content.decode('utf-8'))


    def test_send_get_requests_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        reponse = self.client.get(url)
        self.assertEqual(reponse.status_code, 404)