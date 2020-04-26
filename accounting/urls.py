from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'accounting'

urlpatterns = [
      path('', views.index, name='index'),
      path('clients', views.clients, name='clients'),
      path('clients/create', views.client_create, name='client_create'),
      path('clients/<uuid:uuid>', views.client, name='client'),
      path('clients/update/<uuid:uuid>', views.client_update, name='client_update'),

      path('company/create', views.company_create, name='company_create'),

      path('items', views.items, name='items'),
      path('items/create', views.item_create, name='item_create'),

      path('invoices', views.invoices, name='invoices')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
