from django.db import models


class MotivoContactoChoices(models.TextChoices):
    CONSULTA_GENERAL = 'Consulta general', 'Consulta general'
    PROBLEMA_TECNICO = 'Problema técnico', 'Problema técnico'
    SUGERENCIA = 'Sugerencia', 'Sugerencia'
    OTRO = 'Otro', 'Otro'


class Contacto(models.Model):
    nombre_completo = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    motivo = models.CharField(max_length=30, choices=MotivoContactoChoices.choices)
    mensaje = models.CharField(max_length=500)
    tracked = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contactos'
        ordering = ['tracked', '-fecha_creacion']

    def __str__(self):
        return f'{self.motivo} - {self.correo_electronico}'
