from django.db import models


class Contacto(models.Model):
    email = models.EmailField()
    asunto = models.CharField(max_length=100)
    mensaje = models.CharField(max_length=500)
    tracked = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contactos'
        ordering = ['tracked', '-fecha_creacion']

    def __str__(self):
        return f'{self.asunto} - {self.email}'
