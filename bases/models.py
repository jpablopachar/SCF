from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey


class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)
    usuarioCrea = models.ForeignKey(User, on_delete=models.CASCADE)
    usuarioModifica = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True


class ClaseModelo2(models.Model):
    estado = models.BooleanField(default=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)
    usuarioCrea = UserForeignKey(auto_user_add=True, related_name='+')
    usuarioModifica = UserForeignKey(auto_user_add=True, related_name='+')

    class Meta:
        abstract = True
