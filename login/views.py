from django.shortcuts import render, reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from login.models import PasswordResetRequest


def login(request):
    context = {}

    if request.method == "POST":
        user = authenticate(request, username=request.POST['user'], password=request.POST['password'])
        if user:
            dj_login(request, user)
            return HttpResponseRedirect(reverse('accounting:index'))
        else:
            context = {
                'error': 'Bad username or password.'
            }
    return render(request, 'login/login.html', context)


def logout(request):
    dj_logout(request)
    return HttpResponseRedirect(reverse('login:login'))


def password_reset(request):
    pass


def sign_up(request):
    context = {}
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_name = request.POST['user']
        email = request.POST['email']
        if password == confirm_password:
            if User.objects.create_user(user_name, email, password):
                return HttpResponseRedirect(reverse('login:login'))
            else:
                context = {
                    'error': 'Could not create user account - please try again.'
                }
        else:
            context = {
                'error': 'Passwords did not match. Please try again.'
            }

    return render(request, 'login/sign_up.html', context)


@login_required()
def sign_up_two(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk)
        user.last_name = request.POST['last_name']
        user.first_name = request.POST['first_name']
        user.save()

        return HttpResponseRedirect(reverse('accounting:company_create'))

    return render(request, 'login/sign_up_two.html')


def request_password_reset(request):
    if request.method == "POST":
        post_user = request.POST['username']
        user = None

        if post_user:
            try:
                user = User.objects.get(username=post_user)
            except:
                print(f"Invalid password request: {post_user}")
        else:
            post_user = request.POST['email']
            try:
                user = User.objects.get(email=post_user)
            except User.DoesNotExist:
                print(f"Invalid password request: {post_user}")
        if user:
            prr = PasswordResetRequest()
            prr.user = user
            prr.save()
            print(prr)

            send_mail(
                'Reset your password',
                F"This is your reset link: {reverse('login:password_reset')}/{prr}",
                'login@django.com',
                [user.email],
                fail_silently=False,
            )

            return HttpResponseRedirect(reverse('login:password_reset'))

    return render(request, 'login/request_password_reset.html')


def password_reset(request):
    if 'token' in request.GET:
        context = {
            'token': request.GET['token']
        }
    else:
        context = {}

    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if request.user.is_authenticated:
                user = request.user

            else:
                token = request.POST['token']

                try:
                    prr = PasswordResetRequest.objects.get(token=token)
                    prr.save()

                except PasswordResetRequest.DoesNotExist:
                    print("Invalid password reset attempt.")
                    return render(request, 'login/password_reset.html')

                user = prr.user

        user.set_password(password)
        user.save()
        return HttpResponseRedirect(reverse('login:login'))

    return render(request, 'login/password_reset.html', context)


@login_required
def delete_account(request):
    if request.method == "POST":
        if request.POST['confirm_deletion'] == "DELETE":
            user = authenticate(request, username=request.user.username, password=request.POST['password'])
            if user:
                print(f"Deleting user {user}")
                user.delete()
                return HttpResponseRedirect(reverse('login:login'))
            else:
                print("fail delete")

    return render(request, 'login/delete_account.html')
