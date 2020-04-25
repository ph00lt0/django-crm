from django.db import models
from django.contrib.auth.models import User
import uuid


class Company(models.Model):
    name = models.CharField(max_length=255)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)


class CompanyDetail(models.Model):
    company_id = models.OneToOneField(Company, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=8)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    vat = models.CharField(max_length=200)
    commerce = models.CharField(max_length=200)
    logo = models.IntegerField()


class Currency(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=3)


class BankAccount(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.IntegerField()
    name = models.CharField(max_length=200)
    iban = models.CharField(max_length=34)
    currency_id = models.ForeignKey(Currency, on_delete=models.PROTECT)


class Client(models.Model):
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.PROTECT)


class ClientDetail(models.Model):
    client_id = models.OneToOneField(Client, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=8)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    logo = models.IntegerField()
    vat = models.CharField(max_length=200)
    commerce = models.CharField(max_length=200)


class Invoice(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.PROTECT)
    reference = models.CharField(max_length=35)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    dPaid = models.DateField()
    dSent = models.DateField()
    dViewed = models.DateField()


class Item(models.Model):
    description = models.TextField()
    default_price = models.DecimalField(decimal_places=2, max_digits=20)
    company_id = models.ForeignKey(Company, on_delete=models.PROTECT)


class InvoiceItem(models.Model):
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    amount = models.IntegerField()
