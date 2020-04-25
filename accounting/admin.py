from django.contrib import admin
from .models import Employee, Client, ClientDetail, Company, CompanyDetail, Currency, BankAccount, Invoice, InvoiceItem, Item


admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(ClientDetail)
admin.site.register(Company)
admin.site.register(CompanyDetail)
admin.site.register(Currency)
admin.site.register(BankAccount)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Item)
