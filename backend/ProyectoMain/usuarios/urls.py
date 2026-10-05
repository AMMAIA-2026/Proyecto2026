from django.urls import path

from .views import (
    RecuperarPasswordView,
    RegistroView,
    UsuarioDetailView,
    UsuarioListView,
)


urlpatterns = [
    path('registro/', RegistroView.as_view(), name='usuario-registro'),
    # Deshabilitado: prueba piloto. A futuro se usará token temporal.
    # path(
    #     'recuperar-password/',
    #     RecuperarPasswordView.as_view(),
    #     name='usuario-recuperar-password',
    # ),
    path('', UsuarioListView.as_view(), name='usuario-list'),
    path('<int:usuario_id>/', UsuarioDetailView.as_view(), name='usuario-detail'),
]
