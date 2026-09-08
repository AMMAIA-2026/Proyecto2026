from django.urls import path

from .views import InscribirseCampaniaView


urlpatterns = [
    path(
        'campanias/<int:campania_id>/',
        InscribirseCampaniaView.as_view(),
        name='inscribirse-campania',
    ),
]
