from django.shortcuts import reverse
from functools import wraps
from django.http import HttpResponseRedirect
from django.contrib import messages


def employee_check(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        if not hasattr(request.user, 'employee'):
            messages.add_message(request, messages.ERROR, F"User has no company assigned.")
            return HttpResponseRedirect(reverse('accounting:company_create'))

        return function(request, *args, **kwargs)
    return wrap
