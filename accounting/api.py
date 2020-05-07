from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Invoice, Client, InvoiceItem
from .serializers import InvoiceSerializer, InvoiceDetailSerializer
from .permissions import IsOwnerOrNoAccess


# generics.ListCreateAPIView
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.action == 'list':
            return InvoiceSerializer
        if self.action == 'retrieve':
            return InvoiceDetailSerializer
        return InvoiceDetailSerializer

    def get_queryset(self):
        client_items = Client.objects.filter(company=self.request.user.employee.company)
        queryset = Invoice.objects.filter(client__in=client_items.values_list('pk'))
        return queryset
