from django.urls import path
from .views import CampaniaDetailView, CampaniaListCreateView


urlpatterns = [
    path('', CampaniaListCreateView.as_view(), name='campania-list-create'),
    path(
        '<int:campania_id>/',
        CampaniaDetailView.as_view(),
        name='campania-detail',
    ),
]
