from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from account.forms import AccountSignUpForm

User = get_user_model()

class AccountCreateViewTests(TestCase):

    def setUp(self):
        self.signup_url = reverse('signup')

    def test_signup_page_loads(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup_form.html')
        self.assertIsInstance(response.context['form'], AccountSignUpForm)

    def test_signup_form_success(self):
        data = {
            'cpf': '123.456.789-00',
            'email': 'newuser@example.com',
            'password': 'strongpassword123',
            'name': 'New User'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # Check that the user was created
        user = User.objects.get(email='newuser@example.com')
        self.assertTrue(user.check_password('strongpassword123'))
        self.assertEqual(user.cpf, '123.456.789-00')
        self.assertEqual(user.name, 'New User')

    def test_signup_form_invalid_data(self):
        data = {
            'cpf': '123.456.789-00',
            'email': 'invalidemail',  # Invalid email
            'password': 'strongpassword123',
            'name': 'New User'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup_form.html')
        self.assertFalse(User.objects.filter(email='invalidemail').exists())

        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('Informe um endereço de email válido.', form.errors['email'])
