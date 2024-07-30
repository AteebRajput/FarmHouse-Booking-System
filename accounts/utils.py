# emails.py
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_account_activation_email(email, email_token):
    try:
        subject = 'Your account needs to be verified'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = f'Hi, click on the link to activate your account: http://127.0.0.1:8000/accounts/activate/{email_token}'
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False
    return True
