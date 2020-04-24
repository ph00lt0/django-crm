from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_up/2', views.sign_up_two, name='sign_up_two'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('request_password_reset/', views.request_password_reset, name='request_password_reset'),
    path('password_reset/', views.password_reset, name='password_reset'),
]
