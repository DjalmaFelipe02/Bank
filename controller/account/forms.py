from django import forms 
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountSignUpForm(forms.ModelForm):
    password = forms.CharField(label= "Senha",max_length= 50,widget= forms.PasswordInput())    
    class Meta:
        model = User
        fields = ("name", "email","cpf","password",)
        widgets ={
            'cpf' : forms.TextInput(attrs={'data-mask':"000.000.000-00"})
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if User.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está registrado.")
        # Adicione aqui uma função para validar a formatação e a validade do CPF, se necessário.
        return cpf
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este Email já está registrado.")
        # Adicione aqui uma função para validar a formatação e a validade do CPF, se necessário.
        return email
