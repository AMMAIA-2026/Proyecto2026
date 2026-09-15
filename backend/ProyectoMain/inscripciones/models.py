from django.db import models
from usuarios.models import Usuario
from campanias.models import Campania

# Create your models here.
class Inscripcion(models.Model):
        usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
        campania = models.ForeignKey(
        Campania,
        on_delete=models.CASCADE
    )
        fecha_inscripcion = models.DateTimeField(auto_now_add=True)

        class Meta:
            db_table = 'inscripciones'
            constraints = [
                models.UniqueConstraint(
                    fields=['usuario', 'campania'],
                    name='inscripcion_unica_usuario_campania',
                )
            ]
        
        def __str__(self):
            return f"{self.usuario} - {self.campania}"
        
