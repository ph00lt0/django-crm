from .models import Invoice, InvoiceViewed, Employee
from django.utils.deprecation import MiddlewareMixin

import re


class InvoiceMiddleware(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        url = request.path.split('/')
        if request.user.is_anonymous:
            return None
        if Employee.objects.get(user=request.user) or request.user.is_staff:
            print('x')
            return None
        if len(url) < 4:
            return None
        path = url[3]
        if not url[3] == "invoice":
            return None

        try:
            invoice = Invoice.objects.get(uuid=url[4])
            InvoiceViewed.objects.get_or_create(invoice=invoice)
        except Invoice.DoesNotExist:
            return None

        return None
