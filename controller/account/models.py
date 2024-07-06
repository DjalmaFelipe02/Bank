from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given cpf, email, and password.
        """
        if not cpf:
            raise ValueError(_('The CPF must be set'))
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given cpf, email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(cpf, email, password, **extra_fields)

class CustomUser(AbstractUser):

    cpf = models.CharField("CPF", max_length=14, unique=True)
    first_name = None
    last_name = None
    username = None
    name = models.CharField(('Nome'),max_length=70 , unique=False)
    email = models.EmailField(("email"), max_length=50, unique=True)
    value = models.FloatField(default=15.00) #Inicial value Account

    USERNAME_FIELD = "cpf"          #The form field will have the input id declared as "username_id", even though it is a CPF field
    REQUIRED_FIELDS = ["name","email"]

    objects = CustomUserManager()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.value = 15
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'Users'
    
