from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/', views.clients, name='clients'),
    path('clients/create', views.client_create, name='client_create'),
    path('clients/<uuid:uuid>', views.client, name='client'),
    path('company/create', views.company_create, name='company_create'),
]
