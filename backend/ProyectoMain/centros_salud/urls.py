from django.urls import path

from .views import CentroSaludListView


urlpatterns = [
    path('', CentroSaludListView.as_view(), name='centro-salud-list'),
]
