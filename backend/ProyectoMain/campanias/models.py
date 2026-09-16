from django.db import models


class CentroSalud(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    barrio = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    sitio_web = models.URLField(max_length=250, blank=True)
    latitud = models.CharField(max_length=30, blank=True)
    longitud = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.nombre


class Estado_Campania(models.Model):
    estado=models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.estado

class Campania(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1500)
    ubicacion = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado_campania = models.ForeignKey('Estado_Campania', on_delete=models.PROTECT, null=False)
    centro_salud = models.ForeignKey(
        'CentroSalud',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    cupo_maximo = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.titulo
