import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render

from common.utilities import convert_string_to_time
from contests.models import Contest, ContestManager
from contests import service
# Create your views here.


def contests(request):
    return HttpResponse(json.dumps(service.contests()), content_type='application/json')


@login_required
def create(request):
    result = {'success': False}
    if not request.user.is_superuser and not request.user.can_create_contest:
        raise Http404
    if request.method == 'POST':
        if not 'name' in request.POST:
            return HttpResponse(json.dumps(result), content_type='application/json')
        name = request.POST['name']
        if not name:
            return HttpResponse(json.dumps(result), content_type='application/json')
        contest = Contest()
        contest.name = request.POST['name']
        if 'from_time' in request.POST:
            contest.from_time = convert_string_to_time(
                request.POST['from_time'])
        if 'to_time' in request.POST:
            contest.to_time = convert_string_to_time(request.POST['to_time'])
        contest.save()
        result['success'] = True
        result['id'] = contest.id
    return HttpResponse(json.dumps(result), content_type='application/json')


def update(request):
    pass


def delete_contest(request):
    pass
