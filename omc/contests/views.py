import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

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
        raise PermissionDenied
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
            print contest.from_time
        if 'to_time' in request.POST:
            contest.to_time = convert_string_to_time(request.POST['to_time'])
        contest.save()
        manager = ContestManager(contest=contest, user=request.user)
        manager.save()
        result['success'] = True
        result['id'] = contest.id
    return HttpResponse(json.dumps(result), content_type='application/json')


def update_time(contest, field, time_str):
    time = convert_string_to_time(time_str)
    setattr(contest, field, time)


@login_required
def update(request):
    result = {'success': False}
    if not request.user.is_superuser and not request.user.can_create_contest:
        raise PermissionDenied
    if not 'id' in request.GET:
        raise Http404
    contest = get_object_or_404(Contest, pk=request.GET['id'])
    if not service.check_contest_permission(contest, request.user):
        raise PermissionDenied
    if request.method == 'POST':
        for f in Contest.get_field_list():
            if f in request.POST:
                try:
                    if f == 'from_time' or f == 'to_time':
                        update_time(contest, f, request.POST[f])
                    else:
                        setattr(activity_obj, f, request.POST[f])
                except:
                    pass
        contest.save()
        result['success'] = True
    return HttpResponse(json.dumps(result), content_type='application/json')


def delete_contest(request):
    pass
