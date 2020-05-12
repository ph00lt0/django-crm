from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from .models import Invoice, Client, InvoiceItem
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


# generics.ListCreateAPIView
class InvoiceViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.action == 'list':
            return InvoiceSerializer
        if self.action == 'retrieve':
            return InvoiceDetailSerializer
        if self.action == 'create':
            return InvoiceCreateSerializer
        return InvoiceDetailSerializer

    def get_queryset(self):
        client_items = Client.objects.filter(company=self.request.user.employee.company)
        queryset = Invoice.objects.filter(client__in=client_items.values_list('pk'))
        return queryset


class ClientApiView(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.filter(company=self.request.user.employee.company)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # attr = list(request.data.keys())[0]
        # request.data['details'] = {attr: request.data[attr]}
        # print(request.data)

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated client successfully"})

        else:
            return Response({"message": "Failed", "details": serializer.errors})
