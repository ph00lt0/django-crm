from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .models import Client, ClientDetail, Company, CompanyDetail, Employee
from .decorators import employee_check
from .serializers import ClientSerializer

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
    if not client_item.company_id == request.user.employee.company_id:
        return HttpResponseRedirect(reverse('accounting:clients'))

    client_details = get_object_or_404(ClientDetail, client_id=client_item.id)
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
    if not client_item.company_id == request.user.employee.company_id:
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
