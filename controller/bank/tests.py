from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from extract.models import Values
from django.contrib.messages import get_messages

class IndexViewTestCase(TestCase):
    def test_index_view_authenticated(self):
        user = get_user_model().objects.create_user(cpf='123.456.789-00', email='testuser@example.com', password='password')
        self.client.login(cpf='123.456.789-00', password='password')
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('home'))

class HomeViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(cpf='123.456.789-00', email='testuser@example.com', password='password')
        self.client.login(cpf='123.456.789-00', password='password')
        
        now = timezone.now()
        Values.objects.create(value=100, description='Initial deposit', account=self.user, sender=self.user, recipient=self.user, type='D', date=now)
        Values.objects.create(value=50, description='Groceries', account=self.user, sender=self.user, recipient=self.user, type='O', date=now)
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/home.html')
        
        self.assertContains(response, 'Você foi Logado com Sucesso!!!')

        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['user_balance'], 15)
        self.assertEqual(response.context['total_entradas_recebidas'], 100)
        self.assertEqual(response.context['total_saidas_recebidas'], 50)
        self.assertEqual(response.context['entradas_mes'], 100)
        self.assertEqual(response.context['saidas_mes'], 50)
        self.assertEqual(response.context['quantia_livre'], 50)

