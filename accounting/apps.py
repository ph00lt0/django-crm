from django.apps import AppConfig


class AccountingConfig(AppConfig):
    name = 'accounting'

    def ready(self):
        from .signals import create_client_account
