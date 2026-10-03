from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class VersionedJWTAuthentication(JWTAuthentication):
    """Rejects access tokens issued before a user's password/session reset."""

    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        token_version = validated_token.get('token_version', 0)

        if token_version != user.token_version:
            raise AuthenticationFailed(
                'La sesión fue revocada. Iniciá sesión nuevamente.',
                code='token_revoked',
            )

        return user
