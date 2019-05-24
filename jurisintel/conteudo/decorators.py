from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def user_allowed(function):
    def wrap(request, *args, **kwargs):
        if request.user.profile.allow_entrance:
            return wrap
        else:
            return HttpResponseRedirect(reverse('accounts:agendamento'))
    return wrap
