from django.http import JsonResponse


def _error_response(status_code, codigo, mensaje):
    return JsonResponse({
        'codigo': codigo,
        'mensaje': mensaje,
        'status_code': status_code,
    }, status=status_code)


def bad_request(request, exception):
    return _error_response(
        400,
        'peticion_invalida',
        'La solicitud no pudo ser procesada.',
    )


def permission_denied(request, exception):
    return _error_response(
        403,
        'permiso_denegado',
        'No tenés permisos para realizar esta operación.',
    )


def page_not_found(request, exception):
    return _error_response(
        404,
        'recurso_no_encontrado',
        'El recurso solicitado no existe.',
    )


def server_error(request):
    return _error_response(
        500,
        'error_interno',
        'Ocurrió un error interno del servidor.',
    )
