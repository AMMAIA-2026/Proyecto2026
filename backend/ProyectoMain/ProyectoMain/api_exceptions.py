from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    codigo = getattr(exc, 'default_code', 'error_api')
    data = response.data

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
