from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse

from contests.models import Contest
from contests import service
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
    return render(request, 'contests/overview.html', {})


def contest_mc_test(request):
    return render(request, 'contests/mc_test.html', {})


def contest_writing_test(request):
    return render(request, 'contests/writing_test.html', {})


@login_required
def contest_admin(request):
    contest = service.get_contest_from_request(request)
    return render(request, 'contests/admin.html', {'contest': contest})


@login_required
def contests(request):
    if not request.user.is_superuser and not request.user.can_create_contest:
        raise Http404
    return render(request, 'contests/contests.html', {})


@login_required
def user(request):
    return render(request, 'users/user.html', {})
