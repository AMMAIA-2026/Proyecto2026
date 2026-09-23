from rest_framework.views import exception_handler
from rest_framework.exceptions import PermissionDenied


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    codigo = getattr(exc, 'default_code', 'error_api')
    data = response.data

    if isinstance(exc, PermissionDenied):
        response.data = {
            'codigo': 'permiso_denegado',
            'mensaje': 'No tenés permisos para acceder a este recurso.',
            'status_code': response.status_code,
        }
        return response

    if isinstance(data, dict):
        data = dict(data)
        data.setdefault('codigo', str(codigo))
        data.setdefault('status_code', response.status_code)
    else:
        data = {
            'codigo': str(codigo),
            'status_code': response.status_code,
            'detalle': data,
        }

    response.data = data
    return response
