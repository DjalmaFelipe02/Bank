from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

class CustomUser(AbstractUser):

    cpf = models.CharField("CPF", max_length=14, unique=True)
    first_name = None
    last_name = None
    username = None
    name = models.CharField(('Nome'),max_length=70 , unique=False)
    email = models.EmailField(("email"), max_length=50, unique=True)
    value = models.FloatField(default=15.00) #Inicial value Account

    USERNAME_FIELD = "cpf"          #The form field will have the input id declared as "username_id", even though it is a CPF field
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.value = 15
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'Users'
    
