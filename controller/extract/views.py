import os
from io import BytesIO # Biblioteca que permite salvar os Bytes em memória, em vez de salvar no disco.
from .models import Values
from weasyprint import HTML
from datetime import datetime
from django.utils import timezone
from django.conf import settings 
from django.shortcuts import render
from django.contrib import messages
from django.http import FileResponse
from account.models import CustomUser
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def new_value(request):
    if request.method == "GET":
        accounts = CustomUser.objects.exclude(id=request.user.id)
        return render(request, 'extracts/new_value.html', {'accounts': accounts})
    elif request.method == "POST":
        value = request.POST.get('value')
        description = request.POST.get('description')
        # account_id = request.POST.get('account')
        recipient_email = request.POST.get('recipient_email')

       # Verifica se o valor é um número válido
        if not value.replace('.', '', 1).isdigit():
            messages.error(request, "O Campo Valor deve ser um número.")
            return redirect('new_value')

        value = round(float(value), 2)


        # Verifica se o saldo é suficiente para a transferência
        if request.user.value < value:
            messages.error(request, "Saldo insuficiente para realizar a transferência.")
            return redirect('new_value')

        if recipient_email == request.user.email:
            messages.error(request, "Você não pode realizar uma transferência para você mesmo.")
            return redirect('new_value')
        
        try:
            recipient_account = CustomUser.objects.get(email=recipient_email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Conta destinatária não encontrada.")
            return redirect('new_value')

        # # Criar uma nova instância de Values para registrar a transferência
        # transfer = Values.objects.create(
        #     value=value,
        #     description=description,
        #     account=request.user,  # A conta do remetente é a conta do usuário atual
        #     sender=request.user,
        #     recipient=recipient_account,
        #     type='O',  # Saída (Out)
        # )
         # Cria uma nova instância de Values para registrar a saída (transação do remetente)
        transfer_out =Values.objects.create(
            value=-value,  # Valor negativo para saída
            description=description,
            account=request.user,
            sender=request.user,
            recipient=recipient_account,
            type='O',  # Saída (Out)
        )

        # Cria uma nova instância de Values para registrar a entrada (transação do destinatário)
        transfer_in =Values.objects.create(
            value=value,  # Valor positivo para entrada
            description=description,
            account=recipient_account,
            sender=request.user,
            recipient=recipient_account,
            type='D',  # Depósito (Deposity)
        )

        # Atualizar o saldo do usuário que envia (saída)
        sender_account = CustomUser.objects.get(id=request.user.id)
        sender_account.value -= float(value)
        sender_account.save()

        # Atualizar o saldo do usuário que recebe (entrada)
        receiver_account = CustomUser.objects.get(id=recipient_account.id)
        receiver_account.value += float(value)
        receiver_account.save()

        messages.success(request, "Transferência realizada com sucesso!")
        return redirect('view_extract')
    
@login_required
def view_extract(request):
    user = request.user
    accounts = CustomUser.objects.all()
    
    # Filtragem por conta, se aplicável
    account_get = request.GET.get('account')
    
    # Obtém o período selecionado pelo usuário (padrão: últimos 7 dias)
    period = request.GET.get('periodo', 'last_7_days')
    if period == 'last_7_days':
        start_date = timezone.now() - timezone.timedelta(days=7)
    elif period == 'last_month':
        start_date = timezone.now() - timezone.timedelta(days=30)
    elif period == 'last_3_months':
        start_date = timezone.now() - timezone.timedelta(days=90)
    else:
        start_date = None
    
    # Filtros de tipo de transferência
    tipo_transferencia = request.GET.get('tipo')
    
    # Filtra valores enviados
    sent_values = Values.objects.filter(sender=user)
    if account_get:
        sent_values = sent_values.filter(recipient__id=account_get)
    if start_date:
        sent_values = sent_values.filter(date__gte=start_date)
    if tipo_transferencia:
        sent_values = sent_values.filter(type=tipo_transferencia)
    
    # Filtra valores recebidos
    received_values = Values.objects.filter(recipient=user)
    if account_get:
        received_values = received_values.filter(sender__id=account_get)
    if start_date:
        received_values = received_values.filter(date__gte=start_date)
    if tipo_transferencia:
        received_values = received_values.filter(type=tipo_transferencia)
    
    # Combina as transações enviadas e recebidas
    values = sent_values.union(received_values).order_by('-date')

    # Aplica a paginação
    paginator = Paginator(values, 10)
    page = request.GET.get('page', 1)
    try:
        values = paginator.page(page)
    except PageNotAnInteger:
        values = paginator.page(1)
    except EmptyPage:
        values = paginator.page(paginator.num_pages)
    
    return render(request, 'extracts/view_extract.html', {'values': values, 'accounts': accounts})


@login_required
def export_pdf(request):
    user = request.user
    values= Values.objects.filter(account=user,date__month=datetime.now().month).order_by('-date')
    accounts = CustomUser.objects.filter(id=user.id)

    # Captura a data e hora atual
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    
    path_template = os.path.join(settings.BASE_DIR, '../views/extracts/partials/extrato.html')# Colocando o caminho do arquivo HYML em uma variável, pois não se pode usar o "extratos.html" como caminho para a função "render_to_string"
    path_output = BytesIO() # Para salvar o Bytes em memória RAM, para assim ja mandar para o ususário e depois elimina-lo da memoria, fazendo com que não gaste espaço em disco na propria máquina.

    template_render = render_to_string(path_template, {'values': values, 'accounts': accounts,'current_time':current_time,'user': user,})# Aqui ele tranforma o HTML do Django em um HTML normal, com os dados dos usuário, e sem as funcoes do Django.
    #print(template_render) ---> Aqui vemos que foi printado no terminal o html sem as funções do django, apenas os valores dos dados.
    #return HttpResponse(template_render)

    HTML(string=template_render).write_pdf(path_output) # Instaciando o HTML no weasyprint, para gerar o seu PDF e ser salvo no "path_output".

    path_output.seek(0) #Voltando o ponteiro para o começo do arquivo, pois se estiver no final ele vai considerar o arquivo vazio, já que ele lê tudo oque estiver na frente do ponteiro.
    #(Ex: É como digitar em um rascunho vazio e sempre o ponteiro de digitar irá ficar no final do texto, com esse código, faz o ponteiro retornar para o inicio provando assim a existencia de algo non arquivo).
    
    return FileResponse(path_output, filename="extrato.pdf") # Retorna para o usuário o arquivo PDF
