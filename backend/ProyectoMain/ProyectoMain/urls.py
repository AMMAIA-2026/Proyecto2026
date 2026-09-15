from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from usuarios.views import CustomTokenObtainPairView

handler400 = 'ProyectoMain.error_handlers.bad_request'
handler403 = 'ProyectoMain.error_handlers.permission_denied'
handler404 = 'ProyectoMain.error_handlers.page_not_found'
handler500 = 'ProyectoMain.error_handlers.server_error'

urlpatterns = [
    path('usuarios/', include('usuarios.urls')),
    path('inscripciones/', include('inscripciones.urls')),
    path('campanias/', include('campanias.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('centros-salud/', include('centros_salud.urls')),
    path('contactos/', include('contactos.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
