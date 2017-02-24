from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def contest_overview(request):
    return render(request, 'contests/overview.html', {})


def contest_mc_test(request):
    return render(request, 'contests/mc_test.html', {})


def contest_writing_test(request):
    return render(request, 'contests/writing_test.html', {})


def contest_admin(request):
    return render(request, 'contests/admin.html', {})


def contest_settings(request):
    return render(request, 'contests/settings.html', {})


def user(request):
	return render(request, 'users/user.html', {})