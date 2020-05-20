from rest_framework import serializers
from django.db import transaction
from .models import Item, Invoice, InvoiceItem, Bill, BillItem, Client, ClientDetail, Vendor, VendorDetail, Currency
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDetail
        fields = ['address', 'zip', 'city', 'country', 'email', 'phone', 'vat', 'commerce']


class ClientCreateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDetail
        fields = ['client', 'address', 'zip', 'city', 'country', 'email', 'phone', 'vat', 'commerce']


class ClientSerializer(serializers.ModelSerializer):
    details = ClientDetailSerializer()

    class Meta:
        model = Client
        fields = ['uuid', 'name', 'details']

    @transaction.atomic
    def create(self, data):
        details_data = data.pop('details')
        client = self.Meta.model.objects.create(company=self.context['request'].user.employee.company, **data)
        details_data['client'] = client.pk

        detail_serializer = ClientCreateDetailSerializer(data=details_data)
        if detail_serializer.is_valid():  # PageSerializer does the validation
            detail_serializer.save()
        else:
            raise serializers.ValidationError(detail_serializer.errors)  # throws errors if any
        return client


class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetail
        fields = ['address', 'zip', 'city', 'country', 'email', 'phone', 'vat', 'commerce']


class VendorCreateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetail
        fields = ['vendor', 'address', 'zip', 'city', 'country', 'email', 'phone', 'vat', 'commerce']


class VendorSerializer(serializers.ModelSerializer):
    details = VendorDetailSerializer()

    class Meta:
        model = Vendor
        fields = ['uuid', 'name', 'details']

    @transaction.atomic
    def create(self, data):
        details_data = data.pop('details')
        vendor = self.Meta.model.objects.create(company=self.context['request'].user.employee.company, **data)
        details_data['vendor'] = vendor.pk

        detail_serializer = VendorCreateDetailSerializer(data=details_data)
        if detail_serializer.is_valid():  # PageSerializer does the validation
            detail_serializer.save()
        else:
            raise serializers.ValidationError(detail_serializer.errors)  # throws errors if any
        return vendor


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['description', 'uuid', 'default_price']


class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['description', 'default_price']

    def create(self, data):
        data['company'] = self.context['request'].user.employee.company
        try:
            self.Meta.model.objects.create(**data)
        except:
            return {'status': 'ERROR', 'message': 'Could not create item'}
        return {'status': 'SUCCESS', 'message': ''}


class InvoiceItemSerializer(serializers.ModelSerializer):
    details = ItemSerializer(source='item')

    class Meta:
        model = InvoiceItem
        fields = ['price', 'amount', 'details']


class InvoiceSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField(method_name='get_total_price')
    client = serializers.CharField(source="client.name")

    class Meta:
        model = Invoice
        fields = ['uuid', 'reference', 'client', 'total', 'currency']

    def get_total_price(self, instance):
        items = InvoiceItem.objects.filter(invoice=instance)
        total = 0

        for item_item in items:
            total += item_item.price * item_item.amount
        return total


class InvoiceDetailSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, label='items')
    client = serializers.CharField(source="client.name")

    class Meta:
        model = Invoice
        fields = ['uuid', 'reference', 'client', 'items', 'currency']

    # def update(self, request, *args, **kwargs):
    #     invoice = Invoice.objects.get(uuid=self['uuid'].value)
    #     for invoice_item in args:
    #         print(invoice_item)
    #         invoice_item['invoice'] = invoice.pk
    #         items = invoice_item['items']
    #         invoice_item['price'] = items[0]['price']
    #         invoice_item['amount'] = items[0]['amount']
    #
    #         item_serializer = InvoiceItemCreateItemSerializer(data=invoice_item)
    #         if item_serializer.is_valid():  # PageSerializer does the validation
    #             item_serializer.save()
    #         else:
    #             raise serializers.ValidationError(item_serializer.errors)  # throws errors if any
    #         return self


# validate input for items when creating new invoice
class InvoiceItemCreateSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source="item.uuid")

    class Meta:
        model = InvoiceItem
        fields = ['price', 'amount', 'item']

    # def create(self, data):
    #     item_data = data.pop('item')
    #     item_item = get_object_or_404(Item, uuid=item_data['uuid'])
    #     data['item'] = item_item
    #
    #     item = self.Meta.model.objects.create(**data)
    #     return item


# validate input for items when creating new invoice's items
class InvoiceItemCreateItemSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source="item.uuid")

    class Meta:
        model = InvoiceItem
        fields = ['price', 'amount', 'item', 'invoice']

    def create(self, data):
        item_data = data.pop('item')
        item_item = get_object_or_404(Item, uuid=item_data['uuid'])
        data['item'] = item_item

        item = self.Meta.model.objects.create(**data)
        return item


class InvoiceCreateSerializer(serializers.ModelSerializer):
    items = InvoiceItemCreateSerializer(many=True)
    client = serializers.CharField(source="client.uuid")

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.context['request'].method == 'GET':
    #         self.fields['items'] = InvoiceCreateItemSerializer(many=True, label='items')
    #     else:
    #         self.fields['items'] = InvoiceCreateItemSerializer(many=True, label='items')

    class Meta:
        model = Invoice
        fields = ['uuid', 'reference', 'client', 'items', 'currency']

    @transaction.atomic
    def create(self, data):
        invoice_items_data = data.pop('items')
        client = data.pop('client')

        client_item = get_object_or_404(Client, uuid=client['uuid'])
        if not client_item.company == self.context['request'].user.employee.company:
            return {'status': 'ERROR', 'message': 'Client not found'}

        invoice = self.Meta.model.objects.create(client=client_item, **data)

        for invoice_item in invoice_items_data:
            item_data = invoice_item.pop('item')
            invoice_item['item'] = item_data['uuid']
            invoice_item['invoice'] = invoice.pk
            item_serializer = InvoiceItemCreateItemSerializer(data=invoice_item)
            if item_serializer.is_valid():  # PageSerializer does the validation
                item_serializer.save()
            else:
                raise serializers.ValidationError(item_serializer.errors)  # throws errors if any

        return invoice


class BillItemSerializer(serializers.ModelSerializer):
    details = ItemSerializer(source='item')

    class Meta:
        model = BillItem
        fields = ['price', 'amount', 'details']


class BillSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField(method_name='get_total_price')
    vendor = serializers.CharField(source="vendor.name")

    class Meta:
        model = Bill
        fields = ['uuid', 'reference', 'vendor', 'total', 'currency']

    def get_total_price(self, instance):
        items = BillItem.objects.filter(bill=instance)
        total = 0

        for item_item in items:
            total += item_item.price * item_item.amount
        return total


class BillDetailSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True, label='items')
    vendor = serializers.CharField(source="vendor.name")

    class Meta:
        model = Bill
        fields = ['uuid', 'reference', 'vendor', 'items', 'currency']


# validate input for items when creating new bill
class BillItemCreateSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source="item.uuid")

    class Meta:
        model = BillItem
        fields = ['price', 'amount', 'item']


# validate input for items when creating new bill's items
class BillItemCreateItemSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source="item.uuid")

    class Meta:
        model = BillItem
        fields = ['price', 'amount', 'item', 'bill']

    def create(self, data):
        item_data = data.pop('item')
        item_item = get_object_or_404(Item, uuid=item_data['uuid'])
        data['item'] = item_item
        print(data)

        item = self.Meta.model.objects.create(**data)
        return item


class BillCreateSerializer(serializers.ModelSerializer):
    items = BillItemCreateSerializer(many=True)
    vendor = serializers.CharField(source="vendor.uuid")

    class Meta:
        model = Bill
        fields = ['uuid', 'reference', 'vendor', 'items', 'currency']

    @transaction.atomic
    def create(self, data):
        bill_items_data = data.pop('items')
        vendor = data.pop('vendor')

        vendor_item = get_object_or_404(Vendor, uuid=vendor['uuid'])
        if not vendor_item.company == self.context['request'].user.employee.company:
            return {'status': 'ERROR', 'message': 'Vendor not found'}

        bill = self.Meta.model.objects.create(vendor=vendor_item, **data)

        for bill_item in bill_items_data:
            item_data = bill_item.pop('item')
            bill_item['item'] = item_data['uuid']
            bill_item['bill'] = bill.pk
            item_serializer = BillItemCreateItemSerializer(data=bill_item)
            if item_serializer.is_valid():  # PageSerializer does the validation
                item_serializer.save()
            else:
                raise serializers.ValidationError(item_serializer.errors)  # throws errors if any

        return bill
