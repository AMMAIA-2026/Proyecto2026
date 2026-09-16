from django.db import models


class CentroSalud(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    barrio = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    sitio_web = models.URLField(max_length=200, null=True, blank=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=7)
    longitud = models.DecimalField(max_digits=10, decimal_places=7)

    class Meta:
        db_table = 'centros_salud'
        ordering = ['localidad', 'nombre']

    def __str__(self):
        return self.nombre
