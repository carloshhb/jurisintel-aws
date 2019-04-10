# Imports here
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth import logout
from conteudo.models import Case


# Views here


@login_required(login_url='user_login')
def home(request):
    parameters, tag_list = list(), list()
    all_cases = Case.objects.filter(user=request.user).order_by('-created_at')
    for case in all_cases:
        parameters.append([case.pk, [case.titulo, case.resumo]])
        for tag in case.tags.all():
            tag_list.append([case.pk, [tag.__str__()]])

    context = {
        'parameters': parameters,
        'tags': tag_list,
    }

    return render(request, 'conteudo/home.html', context)


def landing_page(request):
    return render(request, 'landing-page.html', {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
