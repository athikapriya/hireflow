from celery import shared_task
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(user_email, user_name):
    subject = "Welcome to HireFlow!"
    message = f"Hi {user_name},\n\nThank you for creating your account on HireFlow!"
    from_email = settings.EMAIL_HOST_USER 
    recipient_list = [user_email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        logger.info(f"Welcome email sent to {user_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {user_email}: {e}")