from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html', {})


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
