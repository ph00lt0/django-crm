from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views
from . import api


# router = routers.DefaultRouter()
# router.register(r'invoice', api.InvoiceViewSet, basename='invoice')

app_name = 'accounting'

invoice_list = api.InvoiceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

invoice_detail = api.InvoiceViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'put': 'update'
})

bill_list = api.BillViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

bill_detail = api.BillViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'put': 'update'
})

urlpatterns = [
      path('', views.index, name='index'),
      path('clients', views.clients, name='clients'),
      path('vendors', views.vendors, name='vendors'),

      path('company/create', views.company_create, name='company_create'),

      path('items', views.items, name='items'),

      path('invoices', views.invoices, name='invoices'),
      path('invoices/<uuid:uuid>', views.invoice, name='invoice'),
      path('invoice/<uuid:uuid>', views.public_invoice, name='invoice'),

      path('bills', views.bills, name='bills'),
      path('bills/<uuid:uuid>', views.bill, name='bill'),

      path('api/v1/rest-auth/', include('rest_auth.urls')),

      path('api/v1/invoice', invoice_list, name='invoice-list'),
      path('api/v1/invoice/<uuid:uuid>', invoice_detail, name='invoice-detail'),
      path('api/public/invoice/<uuid:uuid>', api.PublicInvoice.as_view(), name='invoice-public'),
      path('api/v1/invoice/<uuid:uuid>/<uuid:item>', invoice_detail, name='invoice-detail'),

      path('api/v1/bill', bill_list, name='bill-list'),
      path('api/v1/bill/<uuid:uuid>', bill_detail, name='bill-detail'),
      path('api/v1/bill/<uuid:uuid>/<uuid:item>', bill_detail, name='bill-detail'),

      path('api/v1/item', api.ItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='item-api'),
      path('api/v1/item/<uuid:uuid>', api.ItemViewSet.as_view({'put': 'update'}), name='item-api'),

      path('api/v1/client', api.ClientViewSet.as_view({'get': 'list', 'post': 'create'}), name='clients-api'),
      path('api/v1/client/<uuid:uuid>', api.ClientViewSet.as_view({'put': 'update'}), name='clients-api'),

      path('api/v1/vendor', api.VendorViewSet.as_view({'get': 'list', 'post': 'create'}), name='vendors-api'),
      path('api/v1/vendor/<uuid:uuid>', api.VendorViewSet.as_view({'put': 'update'}), name='vendors-api'),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += router.urls
