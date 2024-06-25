
from django.contrib import admin
from django.urls import path, include # adicionar include
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views

from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("bank.urls")),
    path('', include("account.urls")),
    path('analytics/', include("analytics.urls")),
    path('wallet/', include("wallet.urls")),
    path('account/', include("django.contrib.auth.urls")),
    path('extract/', include('extract.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
