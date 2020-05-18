from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import ClientAccount, Invoice
from django.conf import settings
from rest_framework import HTTP_HEADER_ENCODING


class PasswordLessLogin:
    def authenticate(self, request, username=None, password=None):
        url = request.path.split('/')
        if len(url) < 4:
            return None
        if not url[3] == "invoice":
            return None

        try:
            invoice = Invoice.objects.get(uuid=url[4])
            client = invoice.client
            client_account = ClientAccount.objects.get(client=client)
            user_pk = client_account.user.pk
            print(user_pk)
            user = User.objects.get(id=user_pk)
            login(request, user)
            # user = self.get_user(user_pk)
            print(user)
            return user
        except User.DoesNotExist:
            return None
        except ClientAccount.DoesNotExist:
            return None

    def authenticate_header(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if isinstance(auth, str):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
