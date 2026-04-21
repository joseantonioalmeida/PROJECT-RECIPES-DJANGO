from .base import AuthorsBaseTest
import  pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user',
            password=string_password,
        )

        # usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        #usuario vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Enter your username')
        password_field = self.get_by_placeholder(form, 'Enter your password')
        
        # usuário preenche os dados de login
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # usuário envia o formulário
        form.submit()
        WebDriverWait(self.browser, 10).until(
        EC.presence_of_element_located((By.ID, "django-messages"))
        )

        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn(
            f'You are logged in with {user.username}.',
            body_text,
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text,
        )

    def test_form_login_is_valid(self):
        # usuário abre a página de login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        # e tenta enviar valores vazios
        username = self.get_by_placeholder(form, 'Enter your username')
        password = self.get_by_placeholder(form, 'Enter your password')

        username.send_keys(' ')
        password.send_keys(' ')

        # envia o formulário
        form.submit()

        #vê um mensagem de erro na tela
        self.assertIn(
            'Invalid username or password.',
            self.browser.find_element(By.TAG_NAME, 'body').text,
        )

    def test_form_login_invalid_credentials(self):
        # usuário abre a página de login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        # e tenta enviar valores vazios
        username = self.get_by_placeholder(form, 'Enter your username')
        password = self.get_by_placeholder(form, 'Enter your password')

        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        # envia o formulário
        form.submit()

        #vê um mensagem de erro na tela
        self.assertIn(
            'Invalid credentials.',
            self.browser.find_element(By.TAG_NAME, 'body').text,
        )