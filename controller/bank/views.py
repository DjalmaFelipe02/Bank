from django.shortcuts import render, redirect
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from extract.models import Values 
from django.utils import timezone

def index(request):
    if request.user.is_authenticated:
        # Se o usuário estiver autenticado, redirecione para a página home
        return redirect(reverse('home'))
    else:
        # Caso contrário, continue renderizando a página index
        aviso = "Aviso importante: Esta página não exige Login"
        messages.warning(request, aviso)
        return render(request, "index.html", {'titulo': 'Bem-Vindo ao TreeBank'})


@login_required
def home (request):
    mensagem = " Você foi Logado com Sucesso!!!"
    messages.success(request,mensagem)

    user = request.user  # Obtenha o usuário logado

    # Calcular o saldo da conta do usuário
    user_balance = user.value   

    # Calcular o total de transferências de entrada recebidas pelo usuário
    total_entradas_recebidas = Values.objects.filter(account=user, type='D').aggregate(total=models.Sum('value'))['total'] or 0
    total_saidas_recebidas = Values.objects.filter(account=user, type='O').aggregate(total=models.Sum('value'))['total'] or 0

    # Calcular o total de entradas e saídas do mês atual
    now = timezone.now()
    inicio_mes = now.replace(day=1)
    
    entradas_mes = Values.objects.filter(account=user, type='D', date__gte=inicio_mes).aggregate(total=models.Sum('value'))['total'] or 0
    saidas_mes = Values.objects.filter(account=user, type='O', date__gte=inicio_mes).aggregate(total=models.Sum('value'))['total'] or 0

    # Calcular a quantia livre do mês
    quantia_livre = total_entradas_recebidas - total_saidas_recebidas


    context = {
        'user': user,
        'user_balance': user_balance,  # Adicione o saldo da conta ao contexto
        'total_entradas_recebidas': total_entradas_recebidas,
        'total_saidas_recebidas': total_saidas_recebidas,
        'entradas_mes': entradas_mes,
        'saidas_mes': saidas_mes,
        'quantia_livre': quantia_livre
        }

    return render(request, "bank/home.html",context)


