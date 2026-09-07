from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from usuarios.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('inscripciones/', include('inscripciones.urls')),
    path('campanias/', include('campanias.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('centros-salud/', include('centros_salud.urls')),
    path('contactos/', include('contactos.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
