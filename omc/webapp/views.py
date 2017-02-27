from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse

# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def login(request):
    if request.user.id:
        if 'next' in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        return HttpResponseRedirect(reverse('webapp:index'))
    return render(request, 'login.html', {})

@login_required
def logout(request):
    user_logout(request)
    return HttpResponseRedirect(reverse('webapp:index'))

def contest_overview(request):
    return render(request, 'contest/overview.html', {})


def contest_mc_test(request):
    return render(request, 'contest/mc_test.html', {})


def contest_writing_test(request):
    return render(request, 'contest/writing_test.html', {})


def contest_admin(request):
    return render(request, 'contest/admin.html', {})


def contest_settings(request):
    return render(request, 'contest/settings.html', {})


def contests_management(request):
    return render(request, 'contests_management.html', {})


def user(request):
    return render(request, 'users/user.html', {})
