from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views
from . import api


router = routers.DefaultRouter()
router.register(r'invoice', api.InvoiceViewSet)

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

      path('invoices', views.invoices, name='invoices'),
      path('invoices/create', views.invoice_create, name='invoice_create'),

      # path('api/v1/invoices', InvoiceViewSet.as_view()),
      # path('api/v1/invoices/<uuid:uuid>', InvoiceViewSet.as_view()),
      # path('api/v1/invoices/<int:pk>/', InvoiceDetail.as_view()),
      path('api/v1/rest-auth/', include('rest_auth.urls')),
      path('api/', include(router.urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
