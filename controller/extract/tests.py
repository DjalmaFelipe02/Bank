from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Values
from django.utils import timezone

CustomUser = get_user_model()

class NewValueTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(cpf='123.456.789-00', email='testuser@example.com', password='password', name='Test User', value=15)
        self.recipient = CustomUser.objects.create_user(cpf='098.765.432-11', email='recipient@example.com', password='password', name='Recipient User', value=15)
        self.client.login(cpf='123.456.789-00', password='password')

    def test_get_new_value_page(self):
        response = self.client.get(reverse('new_value'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'extracts/new_value.html')

    def test_post_new_value_success(self):
        response = self.client.post(reverse('new_value'), {
            'value': '5.00',
            'description': 'Test Transfer',
            'recipient_email': 'recipient@example.com'
        })
        self.assertRedirects(response, reverse('view_extract'))
        self.assertEqual(Values.objects.count(), 2)  # Uma transação de saída e uma de entrada
        self.user.refresh_from_db()
        self.recipient.refresh_from_db()
        self.assertEqual(self.user.value, 10)
        self.assertEqual(self.recipient.value, 20)

    def test_post_new_value_insufficient_balance(self):
        response = self.client.post(reverse('new_value'), {
            'value': '20.00',
            'description': 'Test Transfer',
            'recipient_email': 'recipient@example.com'
        })
        self.assertRedirects(response, reverse('new_value'))
        self.assertEqual(Values.objects.count(), 0)
        self.user.refresh_from_db()
        self.assertEqual(self.user.value, 15)

    def test_post_new_value_invalid_value(self):
        response = self.client.post(reverse('new_value'), {
            'value': 'invalid',
            'description': 'Test Transfer',
            'recipient_email': 'recipient@example.com'
        })
        self.assertRedirects(response, reverse('new_value'))
        self.assertEqual(Values.objects.count(), 0)

    def test_post_new_value_self_transfer(self):
        response = self.client.post(reverse('new_value'), {
            'value': '10.00',
            'description': 'Test Transfer',
            'recipient_email': 'testuser@example.com'
        })
        self.assertRedirects(response, reverse('new_value'))
        self.assertEqual(Values.objects.count(), 0)

class ViewExtractTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(cpf='123.456.789-00', email='testuser@example.com', password='password', name='Test User', value=100)
        self.client.login(cpf='123.456.789-00', password='password')

        now = timezone.now()
        
        Values.objects.create(
            value=20,
            description='Recent Value',
            account=self.user,
            sender=self.user,
            recipient=self.user,
            type='D',
            date=now - timezone.timedelta(days=5)
        )
        
        Values.objects.create(
            value=10,
            description='Old Value',
            account=self.user,
            sender=self.user,
            recipient=self.user,
            type='D',
            date=now - timezone.timedelta(days=30)
        )

    def test_view_extract_page(self):
        response = self.client.get(reverse('view_extract'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'extracts/view_extract.html')

    def test_view_extract_filter(self):
        response = self.client.get(reverse('view_extract'), {'periodo': 'last_7_days'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'extracts/view_extract.html')
    
        date_to_check = (timezone.now() - timezone.timedelta(days=8)).strftime('%Y-%m-%d')

        # Verifica se a data não está presente na resposta como string
        self.assertNotContains(response, date_to_check)


class ExportPDFTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(cpf='123.456.789-00', email='testuser@example.com', password='password', name='Test User', value=100)
        self.client.login(cpf='123.456.789-00', password='password')
        self.value = Values.objects.create(
            value=10,
            description='Test Value',
            account=self.user,
            sender=self.user,
            recipient=self.user,
            type='D',
            date=timezone.now()
        )

    def test_export_pdf(self):
        response = self.client.get(reverse('export_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="extrato.pdf"')



