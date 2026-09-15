from rest_framework.permissions import BasePermission
from usuarios.models import RolChoices

class EsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.rol == RolChoices.ADMINISTRADOR
        )


class EsUsuarioEstandar(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.rol == RolChoices.USUARIO_ESTANDAR
        )
        
class EsAdministradorOSiMismo(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return (
            request.user.rol == RolChoices.ADMINISTRADOR
            or obj.pk == request.user.pk
        )
