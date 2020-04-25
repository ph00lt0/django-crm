from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Client, ClientDetail, Company, CompanyDetail, Employee
from .decorators import employee_check

from login.decorators import profile_completed


@login_required()
@profile_completed
def index(request):
    context = {

    }
    return render(request, 'accounting/index.html', context)


# Clients
@login_required()
@employee_check
@profile_completed
def clients(request):
    company_id = request.user.employee.company_id

    client_items = Client.objects.filter(company_id=company_id)

    context = {
        'clients': client_items
    }

    return render(request, 'accounting/clients.html', context)


@login_required()
@employee_check
@profile_completed
def client(request, uuid):
    client_item = get_object_or_404(Client, uuid=uuid)

    context = {
        'client': client_item
    }

    return render(request, 'accounting/client.html', context)


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
            company_id=request.user.employee.company_id
        )
        client_id = Client.objects.latest('id')
        ClientDetail.objects.create(
            client_id=client_id,
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
        company_id = Company.objects.latest('id')
        CompanyDetail.objects.create(
            company_id=company_id,
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
            company_id=company_id,
            user=request.user
        )

    messages.add_message(request, messages.SUCCESS, F"Created company.")
    return HttpResponseRedirect(reverse('accounting:clients'))
