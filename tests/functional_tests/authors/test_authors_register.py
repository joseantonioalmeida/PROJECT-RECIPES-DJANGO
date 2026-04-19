from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest



@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):    
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' '*20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/div/form'
        )
    
    def wait_for_error_message(self, error_message):
        """Aguarda a mensagem de erro aparecer na página usando WebDriverWait"""
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{error_message}')]"))
        )
    
    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@dummy.com')

        callback(form)
        self.sleep()
        return form
    
    def test_empty_first_name_error_message(self):
        def callback(form):      
            first_name_field = self.get_by_placeholder(form, 'Ex: John')
            first_name_field.send_keys(Keys.ENTER)
            self.wait_for_error_message('Write your first name')
        self.form_field_test_with_callback(callback)
    
    def test_empty_last_name_error_message(self):
        def callback(form):      
            last_name_field = self.get_by_placeholder(form, 'Ex: Doe')
            last_name_field.send_keys(Keys.ENTER)
            self.wait_for_error_message('Write your last name')
        self.form_field_test_with_callback(callback)
    
    def test_empty_username_error_message(self):
        def callback(form):      
            username_field = self.get_by_placeholder(form, 'Ex: johndoe')
            username_field.send_keys(Keys.ENTER)
            self.wait_for_error_message('Write your username.')
        self.form_field_test_with_callback(callback)
    
    def test_invalid_email_error_message(self):
        def callback(form):      
            email_field = self.get_by_placeholder(form, 'Ex: johndoe@example.com')
            email_field.clear()
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            self.wait_for_error_message('The e-mail must be valid')
        self.form_field_test_with_callback(callback)
    
    def test_passwords_do_not_match(self):
        def callback(form):      
            password1 = self.get_by_placeholder(form, 'You password')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Different')
            password2.send_keys(Keys.ENTER)
            self.wait_for_error_message('Password and password confirmation do not match.')
        self.form_field_test_with_callback(callback)

    def test_user_valid_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(form, 'Ex: John').send_keys('John')
        self.get_by_placeholder(form, 'Ex: Doe').send_keys('Doe')
        self.get_by_placeholder(form, 'Ex: johndoe').send_keys('johndoe')
        self.get_by_placeholder(form, 'Ex: johndoe@example.com').send_keys('johndoe@example.com')
        self.get_by_placeholder(form, 'You password').send_keys('P@ssw0rd')
        self.get_by_placeholder(form, 'Repeat your password').send_keys('P@ssw0rd')

        form.submit()        
        # # Aguarda a mensagem de sucesso aparecer após o envio do formulário
        self.wait_for_error_message('Your user is created, please log in.')
        self.assertIn(
            'Your user is created, please log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )