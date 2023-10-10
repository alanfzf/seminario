from django.db import models

# Create your models here.
class Hospital(models.Model):
    nombre = models.CharField(max_length=128, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=128, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    nombre = models.CharField(max_length=128, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre
