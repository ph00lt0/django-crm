from rest_framework import serializers
from django.db import transaction
from .models import Item, Invoice, InvoiceItem, Client, ClientDetail, Currency
from django.shortcuts import get_object_or_404
import json


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
        fields = ['description', 'uuid']


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

    @transaction.atomic
    def create(self, data):
        items_data = data.pop('items')
        client = data.pop('client')

        client_item = get_object_or_404(Client, uuid=client['name'])
        if not client_item.company == self.context['request'].user.employee.company:
            return {'status': 'ERROR', 'message': 'Client not found'}

        invoice = self.Meta.model.objects.create(client=client_item, **data)

        # for key in items_data:
        #     item_item = get_object_or_404(Item, uuid=key)
        #     if not item_item.company == self.context['request'].user.employee.company:
        #         return {'status': 'ERROR', 'message': 'Item not found'}
        #
        #     InvoiceItem.objects.create(
        #         invoice=invoice,
        #         item=item_item,
        #         price=item_items[key]['price'],
        #         amount=item_items[key]['amount'],
        #     )
        #     print(item_items[key]['amount'])

        return invoice
