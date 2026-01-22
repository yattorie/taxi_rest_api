import random
from django.conf import settings
from django.core.cache import cache


def generate_code() -> str:
    return str(random.randint(100000, 999999))


def save_code(email: str, code: str) -> None:
    key = f'email_verify:{email}'
    cache.set(
        key=key,
        value=code,
        timeout=settings.EMAIL_VERIFY_CODE_TTL,
    )
