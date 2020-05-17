from django.db import models
from django.contrib.auth.models import User
import uuid


class Currency(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=3)


class Company(models.Model):
    name = models.CharField(max_length=255)
    default_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class CompanyDetail(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=8)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    vat = models.CharField(max_length=200)
    commerce = models.CharField(max_length=200)
    logo = models.IntegerField()


class BankAccount(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.IntegerField()
    name = models.CharField(max_length=200)
    iban = models.CharField(max_length=34)
    currency_id = models.ForeignKey(Currency, on_delete=models.PROTECT)


class Client(models.Model):
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    company = models.ForeignKey(Company, related_name='client_details', on_delete=models.PROTECT)


class ClientDetail(models.Model):
    client = models.OneToOneField(Client, related_name='details', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=8)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    vat = models.CharField(max_length=200)
    commerce = models.CharField(max_length=200)


class ClientAccount(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Invoice(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    reference = models.CharField(max_length=35)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)


class InvoicePaid:
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    date = models.DateField()


class InvoiceViewed:
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    date = models.DateField()


class InvoiceSent:
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    date = models.DateField()


class Item(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    description = models.TextField()
    default_price = models.DecimalField(decimal_places=2, max_digits=20)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='invoice_item_item', on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    amount = models.IntegerField()
