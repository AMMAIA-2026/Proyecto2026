import logging


logger = logging.getLogger('security')

ACCESS_DENIED = 'ACCESS_DENIED'
LOGIN_FAILED = 'LOGIN_FAILED'
OPERATION_BLOCKED = 'OPERATION_BLOCKED'


def mask_email(email):
    # Keep only the first letter and the domain: juan@gmail.com -> j***@gmail.com
    if not email or '@' not in str(email):
        return 'unknown'
    local_part, domain = str(email).split('@', 1)
    return f'{local_part[:1]}***@{domain}'


def log_security_event(request, action, result, detail=None):
    # Never reads request.data or headers, so passwords and tokens are not logged.
    user_id = 'anonymous'
    resource = 'unknown'
    ip = 'unknown'

    if request is not None:
        user = getattr(request, 'user', None)
        if user is not None and user.is_authenticated:
            user_id = user.pk
        resource = f'{request.method} {request.path}'
        ip = request.META.get('REMOTE_ADDR', ip)

    message = (
        f'action={action} user={user_id} resource="{resource}" '
        f'result={result} ip={ip}'
    )
    if detail:
        message += f' {detail}'

    logger.warning(message)
