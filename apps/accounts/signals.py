from django.dispatch import receiver
from djoser.signals import user_registered

from .services.email_verification import generate_code, save_code
from .services.email_sender import send_confirmation_email


@receiver(user_registered)
def send_email_confirmation(sender, user, request, **kwargs):
    code = generate_code()
    save_code(user.email, code)
    send_confirmation_email(user.email, code)
