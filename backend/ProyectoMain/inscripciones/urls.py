from django.urls import path

from .views import (
    CancelarInscripcionView,
    InscribirseCampaniaView,
    MisInscripcionesView,
)


urlpatterns = [
    path(
        'mis-inscripciones/',
        MisInscripcionesView.as_view(),
        name='mis-inscripciones',
    ),
    path(
        'campanias/<int:campania_id>/',
        InscribirseCampaniaView.as_view(),
        name='inscribirse-campania',
    ),
    path(
        '<int:inscripcion_id>/',
        CancelarInscripcionView.as_view(),
        name='cancelar-inscripcion',
    ),
]
