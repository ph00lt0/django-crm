from __future__ import absolute_import, unicode_literals
from crm.celery import app as celery_app

__all__ = ('celery_app',)

default_app_config = 'accounting.apps.AccountingConfig'
