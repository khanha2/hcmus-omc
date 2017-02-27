import json

from django.http import HttpResponse
from django.shortcuts import render

from contests.models import Contest, ContestManager
from contests import service
# Create your views here.


def contests(request):
    return HttpResponse(json.dumps(service.contests()), content_type='application/json')


def create(request):
    pass


def update_contest(request):
    pass


def delete_contest(request):
    pass
