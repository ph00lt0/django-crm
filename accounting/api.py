from rest_framework import viewsets, generics, permissions, status
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import ProtectedError
from django.contrib.auth import login, authenticate
from rest_framework.permissions import AllowAny
from .permissions import IsOwnerOrNoAccess


class PublicInvoice(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'uuid'
    queryset = Invoice.objects.all()
    serializer_class = InvoiceDetailSerializer

    # def get(self, request, *args, **kwargs):
    #     user = authenticate(request)
    #     if user is not None:
    #         print('a')
    #         login(request, user)
    #         return self.get_object()
    #     return Response({"ERROR": "User not authenticated"})


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
            try:
                invoice_item = InvoiceItem.objects.get(item=item_item, invoice=instance)
                invoice_item_serializer = InvoiceItemSerializer(invoice_item, data=request.data, partial=True)
            except InvoiceItem.DoesNotExist:
                data = request.data
                data['invoice'] = instance.pk
                # data['details'] = {"uuid": kwargs['item']}
                data['item'] = str(kwargs['item'])
                print(data)
                invoice_item_serializer = InvoiceItemCreateItemSerializer(data=data)

            if invoice_item_serializer.is_valid():
                invoice_item_serializer.save()
                return Response({'status': 'SUCCESS', 'message': 'Updated invoice item'}, status=status.HTTP_200_OK)
            return Response({"status': 'ERROR', message": "Failed", "details": invoice_item_serializer.errors})

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


class BillViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.action == 'list':
            return BillSerializer
        if self.action == 'retrieve':
            return BillDetailSerializer
        if self.action == 'create':
            return BillCreateSerializer
        return BillDetailSerializer

    def get_queryset(self):
        vendor_items = Vendor.objects.filter(company=self.request.user.employee.company)
        queryset = Bill.objects.filter(vendor__in=vendor_items.values_list('pk'))
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if 'item' not in kwargs:
            instance_serializer = self.get_serializer(instance, data=request.data, partial=True)
            if instance_serializer.is_valid():
                instance_serializer.save()
                return Response({'status': 'SUCCESS', 'message': 'Updated bill'}, status=status.HTTP_200_OK)
            return Response({"status': 'ERROR', message": "Failed", "details": instance.errors})

        else:
            item_item = get_object_or_404(Item, uuid=kwargs['item'])
            bill_item = get_object_or_404(BillItem, item=item_item, bill=instance)

            bill_item_serializer = BillItemSerializer(bill_item, data=request.data, partial=True)
            if bill_item_serializer.is_valid():
                bill_item_serializer.save()
                return Response({'status': 'SUCCESS', 'message': 'Updated bill item'}, status=status.HTTP_200_OK)
            return Response({"status': 'ERROR', message": "Failed", "details": instance.errors})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'item' not in kwargs:
            instance.delete()
            return Response({'status': 'SUCCESS', 'message': 'Updated bill'}, status=status.HTTP_200_OK)
        else:
            item_item = get_object_or_404(Item, uuid=kwargs['item'])
            bill_item = get_object_or_404(BillItem, item=item_item, bill=instance)
            bill_item.delete()
            return Response({'status': 'SUCCESS', 'message': 'Updated bill item'}, status=status.HTTP_200_OK)


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
        return Response({'status': 'SUCCESS', 'message': 'Delete client'}, status=status.HTTP_200_OK)


class VendorViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = VendorSerializer

    def get_queryset(self):
        return Vendor.objects.filter(company=self.request.user.employee.company)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        attr = list(request.data.keys())[0]

        if attr == 'name':
            instance = self.get_serializer(instance, data=request.data, partial=True)
            if instance.is_valid():
                instance.save()
                return Response({'status': 'SUCCESS', 'message': 'Updated vendor'}, status=status.HTTP_200_OK)
            return Response({"status': 'ERROR', message": "Failed", "details": instance.errors})

        else:
            vendor_details = get_object_or_404(VendorDetail, vendor=instance)
            serializer = VendorDetailSerializer(vendor_details, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'SUCCESS', 'message': 'Updated vendor'}, status=status.HTTP_200_OK)
            return Response({'status': 'ERROR', "message": "Failed", "details": serializer.errors})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'status': 'SUCCESS', 'message': 'Deleted vendor'}, status=status.HTTP_200_OK)


class ItemViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.action == 'create':
            return ItemCreateSerializer
        else:
            return ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.filter(company=self.request.user.employee.company)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = self.get_serializer(instance, data=request.data, partial=True)
        if instance.is_valid():
            instance.save()
            return Response({'status': 'SUCCESS', 'message': 'Updated item'}, status=status.HTTP_200_OK)
        return Response({"status': 'ERROR', message": "Failed", "details": instance.errors})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
        except ProtectedError:
            return Response({'status': 'ERROR', 'message': 'Cannot remove items that are used inside an invoice'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'status': 'SUCCESS', 'message': 'Updated invoice'}, status=status.HTTP_200_OK)
