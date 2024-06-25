from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet_list, name='wallet_list'),
    path('create/', views.create_wallet, name='create_wallet'),
    path('<int:wallet_id>/delete/', views.delete_wallet, name='delete_wallet'),
    path('<int:wallet_id>/', views.wallet_detail, name='wallet_detail'),
    path('<int:wallet_id>/add/', views.add_transaction, name='add_transaction'),
    path('<int:wallet_id>/withdraw/', views.withdraw_transaction, name='withdraw_transaction'),
]
