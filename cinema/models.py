
from django.db import models

# Create your models here.

class cartelera(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    

    def __str__(self):
        return self.nombre

class peliculas(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    nuevo = models.BooleanField()
    cartelera = models.ForeignKey(cartelera, on_delete=models.PROTECT)
    fecha_peliculas = models.DateField()
    stock = models.IntegerField()  # Aquí está el campo 'stock'
    imagen = models.ImageField(upload_to='peliculas_imagenes/', null=True)  # Aquí está el campo 'imagen'

    def __str__(self):
        return self.nombre
