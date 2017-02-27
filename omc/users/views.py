import json

from django.contrib.auth import login as user_login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def login(request):
    data = {'success': False}
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            user_login(request, login_form.get_user())
            data['success'] = True
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse(json.dumps(data), content_type='application/json')
