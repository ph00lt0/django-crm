from rest_framework import viewsets, generics, permissions, status
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
        attr = list(request.data.keys())[0]
        if not instance.company == request.user.employee.company:
            return Response({"status': 'ERROR', message": "Failed"}, status=status.HTTP_404_NOT_FOUND)

        if attr == 'name':
            instance = self.get_serializer(instance, data=request.data, partial=True)
            if instance.is_valid():
                instance.save()
                return Response({'status': 'SUCCESS', 'message': 'Updated client'}, status=status.HTTP_200_OK)
            return Response({"status': 'ERROR', message": "Failed", "details": instance.errors})

        else:
            client_details = get_object_or_404(ClientDetail, pk=instance.pk)
            serializer = ClientDetailSerializer(client_details, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'SUCCESS', 'message': 'Updated client'}, status=status.HTTP_200_OK)
            return Response({'status': 'ERROR', "message": "Failed", "details": serializer.errors})

