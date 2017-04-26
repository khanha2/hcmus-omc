import json

from django.contrib.auth import login as user_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render


def login(request):
    data = {'success': False}
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            user_login(request, login_form.get_user())
            data['success'] = True
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def change_password(request):
    data = {'success': False}
    if request.method == 'POST':
        change_form = PasswordChangeForm(request, request.POST)
        if change_form.is_valid():
			form.save()
            data['success'] = True
    return HttpResponse(json.dumps(data), content_type='application/json')
