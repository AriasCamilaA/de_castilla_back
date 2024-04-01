from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from apps.rol.models import Rol

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class CustomUserManager(BaseUserManager):
    def create_user(self, no_documento_usuario, nombre_usuario, apellido_usuario, email=None, password=None, id_rol=None, **extra_fields):
        if not email:
            raise ValueError('El campo de correo electrónico es obligatorio.')
        if not no_documento_usuario:
            raise ValueError('El campo de número de documento es obligatorio.')
        if not nombre_usuario:
            raise ValueError('El campo de nombre de usuario es obligatorio.')
        if not apellido_usuario:
            raise ValueError('El campo de apellido de usuario es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(no_documento_usuario=no_documento_usuario, nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, email=email, id_rol=id_rol, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, no_documento_usuario, nombre_usuario, apellido_usuario, email=None, password=None, id_rol=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(no_documento_usuario, nombre_usuario, apellido_usuario, email, password, id_rol, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    no_documento_usuario = models.BigIntegerField(primary_key=True)
    apellido_usuario = models.CharField(max_length=255, blank=True, null=True)
    celular_usuario = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    nombre_usuario = models.CharField(max_length=255, blank=True, null=True)
    id_rol_fk = models.ForeignKey(Rol, on_delete=models.SET_NULL,db_column='id_rol_fk', null=True)
    estado = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['no_documento_usuario', 'nombre_usuario', 'apellido_usuario', 'id_rol']

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'usuario'

class PasswordResetToken(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Token for {self.user.email}"
