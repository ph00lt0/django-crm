from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Invoice, Client, InvoiceItem
from .serializers import InvoiceSerializer
from .permissions import IsOwnerOrNoAccess


class Invoices(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        client_items = Client.objects.filter(company=self.request.user.employee.company)
        queryset = Invoice.objects.filter(client__in=client_items.values_list('pk'))
        return queryset
