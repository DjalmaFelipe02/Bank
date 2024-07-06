from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from account.models import CustomUser
from extract.models import Values
from django.utils.translation import gettext as _

class AnalyticsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(cpf='123.456.789-01',
                                                   email='testuser1@example.com',
                                                   password='testpass',
                                                   name='Test User 1',
                                                   value=10.00)
        self.client.login(username='123.456.789-01', password='testpass')

        # Criar alguns dados de exemplo para o teste
        self.create_test_data()

    def create_test_data(self):
        # Criar alguns valores para o usuário logado
        today = timezone.now()
        Values.objects.create(value=100.0, description='Depósito 1', date=today, account=self.user, type='D', sender=self.user, recipient=self.user)
        Values.objects.create(value=50.0, description='Saída 1', date=today, account=self.user, type='O', sender=self.user, recipient=self.user)
        

    def test_analytics_function(self):
        # Testar a visualização de analytics para o ano atual
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['monthly_data']), 12)  # Deve haver dados para os 12 meses

        # Verificar os day_ranges para entradas (entries) e saídas (exits)
        for month_data in response.context['monthly_data']:
            self.assertIn('day_ranges', month_data)
            day_ranges = month_data['day_ranges']
            self.assertDayRangeEntriesAndExits(day_ranges)

    def test_analytics_year_filter(self):
        # Testar a visualização de analytics para um ano específico
        year = 2023
        response = self.client.get(reverse('analytics') + f'?year={year}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['monthly_data']), 12)  # Deve haver dados para os 12 meses do ano específico

        # Verificar os day_ranges para entradas (entries) e saídas (exits)
        for month_data in response.context['monthly_data']:
            self.assertIn('day_ranges', month_data)
            day_ranges = month_data['day_ranges']
            self.assertDayRangeEntriesAndExits(day_ranges)

    def test_analytics_i18n(self):
        # Testar a tradução dos nomes dos meses
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Janeiro', response.content.decode())  # Verificar se Janeiro está presente na página

    def test_analytics_performance(self):
        # Testar o desempenho da função de analytics com grandes volumes de dados
        # Criar dados adicionais para testar o desempenho com grandes volumes
        for _ in range(100):  # Criar 100 valores para cada tipo
            Values.objects.create(value=100.0, description='Depósito Teste', date=timezone.now(), account=self.user, type='D', sender=self.user, recipient=self.user)
            Values.objects.create(value=50.0, description='Saída Teste', date=timezone.now(), account=self.user, type='O', sender=self.user, recipient=self.user)

        # Medir o tempo de resposta da visualização de analytics
        import time
        start_time = time.time()
        response = self.client.get(reverse('analytics'))
        end_time = time.time()
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0, msg=f"A execução demorou muito: {execution_time} segundos")  # Verificar se a execução é rápida o suficiente

        # Verificar os day_ranges para entradas (entries) e saídas (exits)
        for month_data in response.context['monthly_data']:
            self.assertIn('day_ranges', month_data)
            day_ranges = month_data['day_ranges']
            self.assertDayRangeEntriesAndExits(day_ranges)

    def assertDayRangeEntriesAndExits(self, day_ranges):
        # Verifica se todos os intervalos de dias estão presentes e contêm 'entries' e 'exits'
        day_ranges_keys = ['1-5', '6-10', '11-15', '16-20', '21-25', '26-31']
        for key in day_ranges_keys:
            self.assertIn(key, day_ranges)
            self.assertIn('entries', day_ranges[key])
            self.assertIn('exits', day_ranges[key])
