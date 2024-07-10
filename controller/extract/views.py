import os
from io import BytesIO  #Biblioteca que permite salvar os Bytes em memória, em vez de salvar no disco.
from datetime import datetime

# from weasyprint import HTML
from xhtml2pdf import pisa
from django.utils import timezone
from django.conf import settings 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import FileResponse ,HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Values
from account.models import CustomUser


@login_required
def new_value(request):
    if request.method == "GET":
        accounts = CustomUser.objects.exclude(id=request.user.id)
        return render(request, 'extracts/new_value.html', {'accounts': accounts})
    elif request.method == "POST":
        value_str = request.POST.get('value')
        description = request.POST.get('description')
        # account_id = request.POST.get('account')
        recipient_email = request.POST.get('recipient_email')
        
       # Verifica se o valor é um número válido
        try:
            value = float(value_str.replace(',', '.'))
        except ValueError:
            messages.error(request, "O campo Valor deve ser um número válido.")
            return redirect('new_value')
        
        if value <= 0:
            messages.error(request, "O campo Valor deve ser um número positivo.")
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
    values = Values.objects.filter(account=user, date__month=datetime.now().month).order_by('-date')
    accounts = CustomUser.objects.filter(id=user.id)

    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")

    # Carregando o template HTML
    template_path = os.path.join(settings.BASE_DIR, '../views/extracts/partials/extrato.html')
    context = {
        'values': values,
        'accounts': accounts,
        'current_time': current_time,
        'user': user,
    }
    template = render_to_string(template_path, context)

    # Criando um buffer de Bytes para salvar o PDF
    buffer = BytesIO()

    # Convertendo o HTML para PDF usando xhtml2pdf
    try:
        pisa_status = pisa.CreatePDF(template, dest=buffer)
    except Exception as e:
        return HttpResponse(f'Erro ao gerar PDF: {str(e)}')

    # Verificando se a conversão foi bem-sucedida
    if pisa_status.err:
        return HttpResponse(f'Erro ao gerar PDF: {pisa_status.err}')

    # Retornando o PDF como resposta HTTP
    buffer.seek(0)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="extrato.pdf"'
    response.write(buffer.getvalue())

    return response