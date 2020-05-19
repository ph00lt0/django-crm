from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Currency, Client, ClientDetail, Company, CompanyDetail, Employee, Item
from .decorators import employee_check
from .tasks import send_email_invoice

from login.decorators import profile_completed


@login_required()
@profile_completed
def index(request):
    send_email_invoice()
    return render(request, 'accounting/index.html')


# Client
@login_required()
@employee_check
@profile_completed
def clients(request):
    return render(request, 'accounting/clients.html')


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
    return render(request, 'accounting/items.html')


# Invoice
@login_required()
@employee_check
@profile_completed
def invoices(request):
    company = request.user.employee.company
    client_items = Client.objects.filter(company=company)
    currency_items = Currency.objects.all()
    item_items = Item.objects.filter(company=company)

    context = {
        'default_currency': company.default_currency.pk,
        'clients': client_items,
        'currencies': currency_items,
        'items': item_items,
    }

    return render(request, 'accounting/invoices.html', context)


@login_required()
@employee_check
@profile_completed
def invoice(request, uuid):
    context = {
        'uuid': uuid
    }
    return render(request, 'accounting/invoice.html', context)


def public_invoice(request, uuid):
    context = {
        'uuid': uuid
    }
    return render(request, 'public_accounting/invoice.html', context)
