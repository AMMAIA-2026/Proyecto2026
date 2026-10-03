import hashlib

from rest_framework.throttling import SimpleRateThrottle


class AccountIPRateThrottle(SimpleRateThrottle):
    """Sliding-window limit by IP and by normalized account, without storing email."""

    rate = None

    def get_rate(self):
        return self.rate

    def parse_rate(self, rate):
        requests, period = rate.split('/', 1)
        amount = int(period[:-1])
        unit = period[-1].lower()
        seconds_by_unit = {
            's': 1,
            'm': 60,
            'h': 60 * 60,
            'd': 24 * 60 * 60,
        }
        if unit not in seconds_by_unit:
            raise ValueError(f'Unidad de throttling no soportada: {unit}')
        return int(requests), amount * seconds_by_unit[unit]

    def account_fingerprint(self, request):
        try:
            email = request.data.get('email', '')
        except Exception:
            email = ''

        normalized_email = str(email).strip().casefold()
        return hashlib.sha256(
            normalized_email.encode('utf-8')
        ).hexdigest()[:16] if normalized_email else 'no-account'

    def allow_request(self, request, view):
        if self.rate is None:
            return True

        self.now = self.timer()
        identifiers = {
            f"ip_{self.get_ident(request)}",
            f"account_{self.account_fingerprint(request)}",
        }
        histories = {}
        blocked_waits = []

        for identifier in identifiers:
            key = self.cache_format % {
                'scope': self.scope,
                'ident': identifier,
            }
            history = self.cache.get(key, [])
            while history and self.now - history[-1] >= self.duration:
                history.pop()
            histories[key] = history
            if len(history) >= self.num_requests:
                blocked_waits.append(
                    max(0, self.duration - (self.now - history[-1]))
                )

        if blocked_waits:
            self.wait_seconds = max(blocked_waits)
            return False

        for key, history in histories.items():
            history.insert(0, self.now)
            self.cache.set(key, history, self.duration)

        self.wait_seconds = None
        return True

    def wait(self):
        return self.wait_seconds


class LoginAttemptThrottle(AccountIPRateThrottle):
    scope = 'login'
    rate = '5/15m'


class PasswordRecoveryThrottle(AccountIPRateThrottle):
    scope = 'password_recovery'
    rate = '3/1h'
