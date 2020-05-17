from django.contrib import admin
from accounting.models import Employee, Client, ClientDetail, ClientAccount, Company, CompanyDetail, Currency, \
    BankAccount, Invoice, InvoiceItem, InvoiceViewed, Item


admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(ClientDetail)
admin.site.register(ClientAccount)
admin.site.register(Company)
admin.site.register(CompanyDetail)
admin.site.register(Currency)
admin.site.register(BankAccount)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(InvoiceViewed)
admin.site.register(Item)
