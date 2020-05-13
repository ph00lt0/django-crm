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
    'put': 'update'
})

urlpatterns = [
      path('', views.index, name='index'),
      path('clients', views.clients, name='clients'),
      # path('clients/create', views.client_create, name='client_create'),
      path('clients/<uuid:uuid>', views.client, name='client'),

      path('company/create', views.company_create, name='company_create'),

      path('items', views.items, name='items'),
      path('items/create', views.item_create, name='item_create'),

      path('invoices', views.invoices, name='invoices'),
      path('invoices/<uuid:uuid>', views.invoice, name='invoice'),
      # path('invoices/create', views.invoice_create, name='invoice_create'),

      path('api/v1/rest-auth/', include('rest_auth.urls')),
      path('api/v1/invoice', invoice_list, name='invoice-list'),
      path('api/v1/invoice/<uuid:uuid>', invoice_detail, name='invoice-detail'),
      path('api/v1/invoice/<uuid:uuid>/<uuid:item>', invoice_detail, name='invoice-detail'),
      # path('api/v1/invoice/item', api.InvoiceItemViewSet.as_view(), name='invoice-item'),
      # path('api/v1/invoice/item/<uuid:item>', api.InvoiceItemViewSet.as_view(), name='invoice-item'),
      path('api/v1/client', api.ClientViewSet.as_view({'get': 'list', 'post': 'create'}), name='clients-api'),
      path('api/v1/client/<uuid:uuid>', api.ClientViewSet.as_view({'put': 'update'}), name='clients-api'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += router.urls
