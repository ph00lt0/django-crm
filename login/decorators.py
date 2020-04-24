from django.shortcuts import reverse
from functools import wraps
from django.http import HttpResponseRedirect


def profile_completed(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        profile = request.user
        if not profile.last_name == '' and not profile.first_name == '':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login:sign_up_two'))

    return wrap
