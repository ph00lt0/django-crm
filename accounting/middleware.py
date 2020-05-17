from .models import Invoice, InvoiceViewed
from django.utils.deprecation import MiddlewareMixin
import re


class InvoiceMiddleware(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        url = request.META['PATH_INFO'].split('/')
        if len(url) < 4:
            return None
        # path = url[3]
        # if re.search("invoice", path):
        #     print(path)
        #     return None

        # invoice = Invoice.objects.get(uuid=url[4])
        # print(invoice)
        # invoice_viewed = InvoiceViewed.objects.get_or_create(invoice=invoice)
        # invoice_viewed.save()

        return None
