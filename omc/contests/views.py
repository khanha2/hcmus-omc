import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

import django_excel as excel
import pyexcel.ext.xls
import pyexcel.ext.xlsx

from common.forms import UploadFileForm
from common.utilities import convert_string_to_time
from contests.models import Contest, ContestManager, MCQuestion, WritingQuestion
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
    setattr(contest, field, str(time))


@login_required
def update(request):
    result = {'success': False}
    contest = service.get_contest_from_request(request)
    if request.method == 'POST':
        for f in Contest.get_field_list():
            if f in request.POST:
                try:
                    if f == 'from_time' or f == 'to_time':
                        update_time(contest, f, request.POST[f])
                    elif f == 'use_mc_test' or f == 'use_writing_test':
                        setattr(contest, f, request.POST[f] == 'true')
                    else:
                        setattr(contest, f, request.POST[f])
                except:
                    pass
        contest.save()
        result['success'] = True
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
def upload_questions(request):
    contest = service.get_contest_from_request(request)
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        if request.POST['type'] == 'mc':
            MCQuestion.objects.filter(contest=contest).delete()
            sheet = request.FILES['file'].get_sheet().get_array()
            for row in sheet[1:]:
                question = MCQuestion(contest=contest)
                i = 0
                for f in MCQuestion.get_field_list():
                    setattr(question, f, row[i])
                    i += 1
                question.save()
        elif request.POST['type'] == 'wt':
            WritingQuestion.objects.filter(contest=contest).delete()
            sheet = request.FILES['file'].get_sheet().get_array()
            for row in sheet[1:]:
                question = WritingQuestion(contest=contest, content=row[0])
                question.save()
    result = {'success': True}
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
def delete_contest(request):
    pass


@login_required
def questions(request):
    contest = service.get_contest_from_request(request)
    result = []
    if 'type' in request.GET:
        if request.GET['type'] == 'mc':
            questions = MCQuestion.objects.filter(contest=contest)
            for q in questions:
                result.append({'id': q.id,
                               'content': q.content,
                               'a': q.a,
                               'b': q.b,
                               'c': q.c,
                               'd': q.d,
                               'answer': q.answer})
        elif request.GET['type'] == 'wt':
            questions = WritingQuestion.objects.filter(contest=contest)
            for q in questions:
                result.append({'id': q.id,
                               'content': q.content})
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
def contestants(request):
    pass


@login_required
def do_contest(request):
    data = {}
    if 'id' in request.GET:
        contest = get_object_or_404(Contest, pk=request.GET['id'])
        if 'generate' in request.GET:
            data = service.generate_match(contest, user)
        # elif 'current' in request.GET:
        #     data = current_match(request, contest_obj)
        # elif 'submit' in request.GET:
        #     data = submit_match(request, contest_obj)
    return HttpResponse(json.dumps(data), content_type='application/json')
