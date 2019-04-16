# Imports here
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth import logout

# Views here


def index(request):
    return render(request, 'index.html', {})


def landing_page(request):
    return render(request, 'landing-page.html', {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def contato(request):
    return render(request, 'contact-us.html', {})
