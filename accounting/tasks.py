from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from time import sleep


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_email_invoice(uuid):
    sender = settings.EMAIL_HOST_USER
    body = F"Open your invoice: {uuid}"
    send_mail('New invoice ready', body, sender, ['test-m66dlxjn7@srv1.mail-tester.com'])
    return None
