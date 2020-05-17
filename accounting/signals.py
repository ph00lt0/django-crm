from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ClientAccount, Client


@receiver(post_save, sender=Client, dispatch_uid="create_client_account")
@transaction.atomic
def create_client_account(sender, instance, **kwargs):
    if not ClientAccount.objects.filter(client=instance).exists():
        user = User()
        user.save()
        client_account = ClientAccount()
        client_account.client = instance
        client_account.user = user
        client_account.save()


@receiver(pre_delete, sender=Client, dispatch_uid='delete_client_account')
def delete_client_account(sender, instance, using, **kwargs):
    if ClientAccount.objects.filter(client=instance).exists():
        client_account = ClientAccount.objects.get(client=instance)
        client_account.user.delete()
