from django.db import transaction
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ClientAccount, Client, ClientDetail, InvoiceSent
from .tasks import send_email_invoice


@receiver(post_save, sender=ClientDetail, dispatch_uid="create_client_account")
@transaction.atomic
def create_client_account(sender, instance, **kwargs):
    if not ClientAccount.objects.filter(client=instance.client).exists():
        user = User()
        user.username = instance.email
        user.email = instance.email
        user.save()
        client_account = ClientAccount()
        client_account.client = instance.client
        client_account.user = user
        client_account.save()


@receiver(pre_delete, sender=Client, dispatch_uid='delete_client_account')
def delete_client_account(sender, instance, **kwargs):
    if ClientAccount.objects.filter(client=instance).exists():
        client_account = ClientAccount.objects.get(client=instance)
        client_account.user.delete()


@receiver(pre_save, sender=InvoiceSent, dispatch_uid='sent_invoice')
def sent_invoice(sender, instance, **kwargs):
    send_email_invoice.delay(instance.invoice.uuid)
