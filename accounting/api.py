from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from .models import Invoice, Client, InvoiceItem
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if 'item' not in kwargs:
            instance_serializer = self.get_serializer(instance, data=request.data, partial=True)
            if instance_serializer.is_valid():
                instance_serializer.save()
                return Response({'status': 'SUCCESS', 'message': 'Updated invoice'}, status=status.HTTP_200_OK)
            return Response({"status': 'ERROR', message": "Failed", "details": instance.errors})

        else:
            item_item = get_object_or_404(Item, uuid=kwargs['item'])
            invoice_item = get_object_or_404(InvoiceItem, item=item_item, invoice=instance)

            invoice_item_serializer = InvoiceItemSerializer(invoice_item, data=request.data, partial=True)
            if invoice_item_serializer.is_valid():
                invoice_item_serializer.save()
                return Response({'status': 'SUCCESS', 'message': 'Updated invoice item'}, status=status.HTTP_200_OK)
            return Response({"status': 'ERROR', message": "Failed", "details": instance.errors})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'item' not in kwargs:
            instance.delete()
            return Response({'status': 'SUCCESS', 'message': 'Updated invoice'}, status=status.HTTP_200_OK)
        else:
            item_item = get_object_or_404(Item, uuid=kwargs['item'])
            invoice_item = get_object_or_404(InvoiceItem, item=item_item, invoice=instance)
            invoice_item.delete()
            return Response({'status': 'SUCCESS', 'message': 'Updated invoice item'}, status=status.HTTP_200_OK)


class ClientViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.filter(company=self.request.user.employee.company)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        attr = list(request.data.keys())[0]

        if attr == 'name':
            instance = self.get_serializer(instance, data=request.data, partial=True)
            if instance.is_valid():
                instance.save()
                return Response({'status': 'SUCCESS', 'message': 'Updated client'}, status=status.HTTP_200_OK)
            return Response({"status': 'ERROR', message": "Failed", "details": instance.errors})

        else:
            client_details = get_object_or_404(ClientDetail, client=instance)
            serializer = ClientDetailSerializer(client_details, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'SUCCESS', 'message': 'Updated client'}, status=status.HTTP_200_OK)
            return Response({'status': 'ERROR', "message": "Failed", "details": serializer.errors})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'status': 'SUCCESS', 'message': 'Updated invoice'}, status=status.HTTP_200_OK)
