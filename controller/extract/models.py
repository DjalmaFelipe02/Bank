from django.db import models
from account.models import *

class Values(models.Model):
    choice_tipo = (
        ('D', 'Deposity'),
        ('O', 'Out')
    )
    
    value = models.FloatField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=choice_tipo)
    sender = models.ForeignKey(CustomUser, related_name='sender', on_delete=models.CASCADE)  # Adicionando campo para o remetente
    recipient = models.ForeignKey(CustomUser, related_name='received_values', on_delete=models.CASCADE)  # Adicionando campo para o destinatário
    
    def __str__(self):
        return self.description
    
    class Meta:
        db_table = 'Values'
