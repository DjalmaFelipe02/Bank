from django.contrib import admin
from .models import Values

# Register your models here.
@admin.register(Values)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields =('value','choice_tipo','date','account')