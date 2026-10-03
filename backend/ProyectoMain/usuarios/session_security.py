from django.db import transaction
from django.db.models import F
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)


@transaction.atomic
def change_password_and_revoke_sessions(user, raw_password):
    """Change a password and invalidate every previously issued session."""
    user.set_password(raw_password)
    user.token_version = F('token_version') + 1
    user.save(update_fields=['password', 'token_version'])
    user.refresh_from_db(fields=['token_version'])

    already_blacklisted = set(
        BlacklistedToken.objects.filter(
            token__user=user,
        ).values_list('token_id', flat=True)
    )
    for outstanding in OutstandingToken.objects.filter(user=user).iterator():
        if outstanding.pk not in already_blacklisted:
            BlacklistedToken.objects.get_or_create(token=outstanding)

    return user
