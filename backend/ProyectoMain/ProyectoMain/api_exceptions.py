from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
)

from .security_log import (
    ACCESS_DENIED,
    OPERATION_BLOCKED,
    log_security_event,
)

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


def _log_denied_request(exc, request, status_code):
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        log_security_event(request, ACCESS_DENIED, status_code)
    elif isinstance(exc, PermissionDenied):
        is_read = request is None or request.method in SAFE_METHODS
        action = ACCESS_DENIED if is_read else OPERATION_BLOCKED
        log_security_event(request, action, status_code)


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    _log_denied_request(exc, context.get('request'), response.status_code)

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
