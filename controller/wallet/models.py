from django.db import models
from django.conf import settings
from account.models import *

class Wallet(models.Model):
    COLOR_CHOICES = [
        ('green', 'Verde'),
        ('blue', 'Azul'),
        ('red', 'Vermelho'),
        ('yellow', 'Amarelo'),
        ('purple', 'Roxo'),
    ]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=6, choices=COLOR_CHOICES)
    balance = models.FloatField(default=0.0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
