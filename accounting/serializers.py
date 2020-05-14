from rest_framework import serializers
from django.db import transaction
from .models import Item, Invoice, InvoiceItem, Client, ClientDetail, Currency
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


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['description', 'uuid', 'default_price']


class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['description', 'default_price']

    def create(self, data):
        try:
            self.Meta.model.objects.create(company=self.context['request'].user.employee.company, **data)
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


# validate input for items when creating new invoice
class InvoiceItemCreateSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source="item.uuid")

    class Meta:
        model = InvoiceItem
        fields = ['price', 'amount', 'item']


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
        print(data)

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
