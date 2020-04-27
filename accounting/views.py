from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

import json

from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .models import Currency, Client, ClientDetail, Company, CompanyDetail, Employee, Item, Invoice, InvoiceItem
from .decorators import employee_check
from .serializers import ClientSerializer

from login.decorators import profile_completed


@login_required()
@profile_completed
def index(request):
    context = {

    }
    return render(request, 'accounting/index.html', context)


# Client
@login_required()
@employee_check
@profile_completed
def clients(request):
    company = request.user.employee.company

    client_items = Client.objects.filter(company=company)

    context = {
        'clients': client_items
    }

    return render(request, 'accounting/clients.html', context)


@login_required()
@employee_check
@profile_completed
def client(request, uuid):
    client_item = get_object_or_404(Client, uuid=uuid)
    if not client_item.company == request.user.employee.company:
        return HttpResponseRedirect(reverse('accounting:clients'))

    client_details = get_object_or_404(ClientDetail, client=client_item)
    client_details.name = client_item.name
    client_details.uuid = client_item.uuid

    context = {
        'client': client_details
    }

    return render(request, 'accounting/client.html', context)


@login_required()
@employee_check
@api_view(['PUT'])
def client_update(request, uuid):
    client_item = get_object_or_404(Client, uuid=uuid)
    if not client_item.company == request.user.employee.company:
        return Response({'Updated client'}, status=status.HTTP_404_NOT_FOUND)

    client_details = get_object_or_404(ClientDetail, pk=client_item.pk)
    attr = request.data['attr']
    value = request.data['value']
    if attr == 'name' and value:
        setattr(client_item, attr, value)
        client_item.save()
        return Response({'status': 'SUCCESS', 'message': 'Updated client'}, status=status.HTTP_200_OK)
    elif attr and value:
        setattr(client_details, attr, value)
        client_details.save()
        return Response({'status': 'SUCCESS', 'message': 'Updated client'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'ERROR', 'message': 'Updated client'}, status=status.HTTP_400_BAD_REQUEST)


@login_required()
@employee_check
@profile_completed
def client_create(request):
    if not request.method == "POST":
        return HttpResponse(status=405)

    # todo add try catch
    with transaction.atomic():
        Client.objects.create(
            name=request.POST['name'],
            company=request.user.employee.company
        )
        client = Client.objects.latest('id')
        ClientDetail.objects.create(
            client=client,
            address=request.POST['address'],
            zip=request.POST['zip'],
            city=request.POST['city'],
            country=request.POST['country'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            vat=request.POST['vat'],
            commerce=request.POST['commerce'],
            logo=0
        )

    messages.add_message(request, messages.SUCCESS, F"Created client.")
    return HttpResponseRedirect(reverse('accounting:clients'))


# Company
@login_required()
@profile_completed
def company_create(request):
    if request.method == "GET":
        if hasattr(request.user, 'employee'):
            messages.add_message(request, messages.INFO, F"You already have a company.")
            return HttpResponseRedirect(reverse('accounting:clients'))
        return render(request, 'accounting/company_create.html')

    if not request.method == "POST":
        return HttpResponse("Method not allowed", status=405)

    # todo add try catch
    with transaction.atomic():
        Company.objects.create(
            name=request.POST['name'],
        )
        company = Company.objects.latest('id')
        CompanyDetail.objects.create(
            company=company,
            address=request.POST['address'],
            zip=request.POST['zip'],
            city=request.POST['city'],
            country=request.POST['country'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            vat=request.POST['vat'],
            commerce=request.POST['commerce'],
            logo=0
        )
        Employee.objects.create(
            company=company,
            user=request.user
        )

    messages.add_message(request, messages.SUCCESS, F"Created company.")
    return HttpResponseRedirect(reverse('accounting:clients'))


# Item
@login_required()
@employee_check
@profile_completed
def items(request):
    item_items = Item.objects.filter(company=request.user.employee.company)

    context = {
        'items': item_items
    }

    return render(request, 'accounting/items.html', context)


@login_required()
@employee_check
@api_view(['POST'])
def item_create(request):
    Item.objects.create(
        description=request.data['description'],
        default_price=request.data['price'],
        company=request.user.employee.company
    )
    return Response({'status': 'SUCCESS', 'message': 'Item created'}, status=status.HTTP_200_OK)


# Invoice
@login_required()
@employee_check
@profile_completed
def invoices(request):
    company = request.user.employee.company
    client_items = Client.objects.filter(company=company)
    invoice_items = Invoice.objects.filter(client__in=client_items.values_list('pk'))
    currency_items = Currency.objects.all()
    item_items = Item.objects.filter(company=company)

    context = {
        'invoices': invoice_items,
        'default_currency': company.default_currency.pk,
        'clients': client_items,
        'currencies': currency_items,
        'items': item_items,
    }

    return render(request, 'accounting/invoices.html', context)


@login_required()
@employee_check
@api_view(['POST'])
def invoice_create(request):
    client_uuid = request.data['client']
    currency_pk = request.data['currency']
    reference = request.data['reference']
    item_json = request.data['items']

    if not client_uuid or not currency_pk or not reference or not item_json:
        return Response({'status': 'ERROR', 'message': 'Fields missing'}, status=status.HTTP_400_BAD_REQUEST)

    client_item = get_object_or_404(Client, uuid=client_uuid)
    currency_item = get_object_or_404(Currency, pk=currency_pk)
    if not client_item.company == request.user.employee.company:
        return Response({'status': 'ERROR', 'message': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

    # todo add try catch
    with transaction.atomic():
        Invoice.objects.create(
            client=client_item,
            reference=reference,
            currency=currency_item,
        )
        invoice = Invoice.objects.latest('id')
        item_items = json.loads(item_json)
        print(item_items)
        for key in item_items:
            # todo create item if not existing
            item_item = get_object_or_404(Item, uuid=key)
            if not item_item.company == request.user.employee.company:
                return Response({'status': 'ERROR', 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

            InvoiceItem.objects.create(
                invoice=invoice,
                item=item_item,
                price=item_items[key]['price'],
                amount=item_items[key]['amount'],
            )
            print(item_items[key]['amount'])

    return Response({'status': 'SUCCESS', 'message': 'Invoice created'}, status=status.HTTP_200_OK)

