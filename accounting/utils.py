from django.contrib import messages


def employee_check(request):
    if not hasattr(request.user, 'employee'):
        messages.add_message(request, messages.ERROR, 'User has no company assigned.')
        return False
    return True
