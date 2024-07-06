from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wallet
from .forms import WalletForm
from account.models import CustomUser

@login_required
def wallet_list(request):
    wallets = Wallet.objects.filter(owner=request.user)
    return render(request, 'wallet/wallet_list.html', {'wallets': wallets})

@login_required
def create_wallet(request):
    if request.method == 'POST':
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.owner = request.user
            wallet.save()
            messages.success(request, 'Carteira criada com sucesso!')
            return redirect('wallet_list')
    else:
        form = WalletForm()
    return render(request, 'wallet/create_wallet.html', {'form': form})

@login_required
def delete_wallet(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, owner=request.user)
    wallet_balance = round(wallet.balance, 2)
    wallet.delete()  # Exclui a carteira

    # Transferir o saldo da carteira de volta para o saldo da conta bancária do usuário
    request.user.value = round(request.user.value + wallet_balance, 2)
    request.user.save()

    messages.success(request, 'Carteira excluída com sucesso e saldo transferido para sua conta.')
    return redirect('wallet_list')

@login_required
def wallet_detail(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, owner=request.user)
    return render(request, 'wallet/wallet_detail.html', {'wallet': wallet})

@login_required
def add_transaction(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, owner=request.user)
    if request.method == 'POST':
        amount_str = request.POST.get('amount', '0')
        try:
            amount = round(float(amount_str),2)
            if request.user.value >= amount:
                wallet.balance = round(wallet.balance + amount, 2)  # Arredondar para 2 casas decimais
                request.user.value = round(request.user.value - amount, 2)  # Arredondar para 2 casas decimais
                wallet.save()
                request.user.save()
                messages.success(request, 'Valor adicionado com sucesso!')
                return redirect('wallet_list')
            else:
                messages.error(request, 'Saldo insuficiente na Conta bancária!')
        except ValueError:
            messages.error(request, 'Valor inserido Inválido!')
    return render(request, 'wallet/add_transaction.html', {'wallet': wallet})

@login_required
def withdraw_transaction(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, owner=request.user)
    if request.method == 'POST':
        amount_str = request.POST.get('amount', '0')
        try:
            amount = round(float(amount_str), 2)  # Arredondar para 2 casas decimais
            if wallet.balance >= amount:
                wallet.balance = round(wallet.balance - amount, 2)  # Arredondar para 2 casas decimais
                request.user.value = round(request.user.value + amount, 2)  # Arredondar para 2 casas decimais
                wallet.save()
                request.user.save()
                messages.success(request, 'Valor retirado com sucesso!')
                return redirect('wallet_list')
            else:
                messages.error(request, 'Valor insuficiente na Carteira!')
        except ValueError:
            messages.error(request, 'Valor inserido Inválido!')
    return render(request, 'wallet/withdraw_transaction.html', {'wallet': wallet})
