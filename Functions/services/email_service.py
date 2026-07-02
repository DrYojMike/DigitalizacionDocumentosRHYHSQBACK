import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_email(subject: str, body: str, recipients: list[str], html: str | None = None) -> bool:
        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients
            )
            if html:
                email.attach_alternative(html, "text/html")
            resultado = email.send()
            return resultado == 1
        except Exception as e:
            logger.exception(e)
            return False