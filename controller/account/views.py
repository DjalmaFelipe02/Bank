from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from account.forms import AccountSignUpForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from django.contrib.auth import get_user_model

User = get_user_model()

class AccountCreateView(CreateView):
    model = User
    template_name = "registration/signup_form.html"
    form_class = AccountSignUpForm
    success_url = reverse_lazy('login')
    # success_message = "Usuário criado com sucesso!!"


    def form_valid(self, form) -> HttpResponse:
        form.instance.password = make_password(form.instance.password)   #Encrypt the password before going to the DataBase
        form.save()
          
        return super(AccountCreateView, self).form_valid(form)
    
    



