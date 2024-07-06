# from django.test import TestCase, Client
# from django.urls import reverse
# from .models import Wallet
# from account.models import CustomUser

# class WalletViewTests(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.user = CustomUser.objects.create_user(
#             cpf='123.456.789-01',
#             email='testuser@example.com',
#             password='testpass',
#             name='Test User',
#             value=10.00  # Valor inicial da conta
#         )
#         self.client.login(cpf='123.456.789-01', password='testpass')
#         self.wallet = Wallet.objects.create(name="Test Wallet", balance=100.00, owner=self.user)

#     def test_wallet_list_view(self):
#         response = self.client.get(reverse('wallet_list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'wallet/wallet_list.html')
#         self.assertContains(response, 'Test Wallet')

#     def test_create_wallet_view_get(self):
#         response = self.client.get(reverse('create_wallet'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'wallet/create_wallet.html')

#     def test_create_wallet_view_post(self):
#         response = self.client.post(reverse('create_wallet'), {
#             'name': 'New Wallet',
#             'balance': '50.00'
#         })
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(Wallet.objects.filter(name='New Wallet').exists())
#         self.assertRedirects(response, reverse('wallet_list'))

#     def test_delete_wallet_view(self):
#         response = self.client.post(reverse('delete_wallet', args=[self.wallet.id]))
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(Wallet.objects.filter(id=self.wallet.id).exists())
#         self.assertRedirects(response, reverse('wallet_list'))
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.value, 115.00)  # Valor inicial + saldo da carteira

#     def test_wallet_detail_view(self):
#         response = self.client.get(reverse('wallet_detail', args=[self.wallet.id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'wallet/wallet_detail.html')
#         self.assertContains(response, 'Test Wallet')

#     def test_add_transaction_view_get(self):
#         response = self.client.get(reverse('add_transaction', args=[self.wallet.id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'wallet/add_transaction.html')

#     def test_add_transaction_view_post(self):
#         self.user.value = 150.00
#         self.user.save()
#         response = self.client.post(reverse('add_transaction', args=[self.wallet.id]), {
#             'amount': '50.00'
#         })
#         self.assertEqual(response.status_code, 302)
#         self.wallet.refresh_from_db()
#         self.assertEqual(self.wallet.balance, 150.00)
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.value, 100.00)
#         self.assertRedirects(response, reverse('wallet_list'))

#     def test_withdraw_transaction_view_get(self):
#         response = self.client.get(reverse('withdraw_transaction', args=[self.wallet.id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'wallet/withdraw_transaction.html')

#     def test_withdraw_transaction_view_post(self):
#         response = self.client.post(reverse('withdraw_transaction', args=[self.wallet.id]), {
#             'amount': '50.00'
#         })
#         self.assertEqual(response.status_code, 302)
#         self.wallet.refresh_from_db()
#         self.assertEqual(self.wallet.balance, 50.00)
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.value, 65.00)  # Valor inicial + saldo transferido da carteira
#         self.assertRedirects(response, reverse('wallet_list'))
from django.test import TestCase, Client
from django.urls import reverse
from .models import Wallet
from account.models import CustomUser

class WalletViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            cpf='123.456.789-01',
            email='testuser@example.com',
            password='testpass',
            name='Test User',
            value=15.00  # Valor inicial da conta
        )
        self.client.login(cpf='123.456.789-01', password='testpass')
        self.wallet = Wallet.objects.create(name="Test Wallet", balance=100.00, owner=self.user, color='blue')

    def test_wallet_list_view(self):
        response = self.client.get(reverse('wallet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/wallet_list.html')
        self.assertContains(response, 'Test Wallet')

    def test_create_wallet_view_get(self):
        response = self.client.get(reverse('create_wallet'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/create_wallet.html')

    def test_create_wallet_view_post(self):
        response = self.client.post(reverse('create_wallet'), {
            'name': 'New Wallet',
            'balance': '50.00',
            'color': 'green'
        })
        self.assertEqual(response.status_code, 302, response.content.decode())
        self.assertTrue(Wallet.objects.filter(name='New Wallet').exists())
        self.assertRedirects(response, reverse('wallet_list'))

    def test_delete_wallet_view(self):
        initial_value = self.user.value
        response = self.client.post(reverse('delete_wallet', args=[self.wallet.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Wallet.objects.filter(id=self.wallet.id).exists())
        self.assertRedirects(response, reverse('wallet_list'))
        self.user.refresh_from_db()
        expected_value = round(initial_value + self.wallet.balance, 2)  # Valor inicial + saldo da carteira
        self.assertEqual(round(self.user.value, 2), expected_value)

    def test_wallet_detail_view(self):
        response = self.client.get(reverse('wallet_detail', args=[self.wallet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/wallet_detail.html')
        self.assertContains(response, 'Test Wallet')

    def test_add_transaction_view_get(self):
        response = self.client.get(reverse('add_transaction', args=[self.wallet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/add_transaction.html')

    def test_add_transaction_view_post(self):
        self.user.value = 150.00
        self.user.save()
        response = self.client.post(reverse('add_transaction', args=[self.wallet.id]), {
            'amount': '50.00'
        })
        self.assertEqual(response.status_code, 302)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 150.00)
        self.user.refresh_from_db()
        self.assertEqual(self.user.value, 100.00)
        self.assertRedirects(response, reverse('wallet_list'))

    def test_withdraw_transaction_view_get(self):
        response = self.client.get(reverse('withdraw_transaction', args=[self.wallet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/withdraw_transaction.html')

    def test_withdraw_transaction_view_post(self):
        response = self.client.post(reverse('withdraw_transaction', args=[self.wallet.id]), {
            'amount': '50.00'
        })
        self.assertEqual(response.status_code, 302)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 50.00)
        self.user.refresh_from_db()
        self.assertEqual(self.user.value, 65.00)  # Valor inicial + saldo transferido da carteira
        self.assertRedirects(response, reverse('wallet_list'))
