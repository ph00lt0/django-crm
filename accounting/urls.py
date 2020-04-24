from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/', views.clients, name='clients'),
]
