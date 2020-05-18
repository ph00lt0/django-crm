from .models import Invoice, InvoiceViewed, Employee
from django.utils.deprecation import MiddlewareMixin


class InvoiceMiddleware(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        url = request.path.split('/')
        if len(url) < 4:
            return None
        if not url[3] == "invoice":
            return None
        # todo change this when authentication is added
        if not request.user.is_anonymous:
            if Employee.objects.get(user=request.user) or request.user.is_staff:
                return None

        try:
            invoice = Invoice.objects.get(uuid=url[4])
            InvoiceViewed.objects.get_or_create(invoice=invoice)
        except Invoice.DoesNotExist:
            return None

        return None
