from django import forms
from .models import Wallet

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'color']
        labels = {
            'name': 'Nome',
            'color': 'Cor'
        }
class WithdrawForm(forms.Form):
    amount = forms.FloatField(label='Retirar', min_value=0.01)