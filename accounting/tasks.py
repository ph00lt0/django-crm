from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from time import sleep



@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_email_invoice():
    sender = settings.EMAIL_HOST_USER
    print(sender)
    send_mail('Celery mail working', 'This is the body', sender, ['test-wta3nodui@srv1.mail-tester.com'])
    return None
