from django.db import models

# Create your models here.

class Cliente(models.Model):
    codigo = models.CharField(max_length=200, unique=True, null=True, blank=False)
    nombre = models.CharField(max_length=200, null=True, blank=False)
    telefono = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=255, unique=True, null=True, blank=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
    costo = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        order_with_respect_to = 'descripcion'   

    def __str__(self):
        return self.descripcion

