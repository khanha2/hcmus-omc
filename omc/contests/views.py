import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

import django_excel as excel

from common.forms import UploadFileForm
from common.utilities import convert_string_to_time, in_range
from contests.models import Contest, Contestant, ContestManager, MCQuestion, WritingQuestion, Match
from contests import resource, service


def contests(request):
    return HttpResponse(json.dumps(service.contests(request)), content_type='application/json')


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
    contest = service.get_contest_from_request(request, True)
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
    contest = service.get_contest_from_request(request, True)
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
    contest = service.get_contest_from_request(request, True)
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
    contest = service.get_contest_from_request(request, True)
    page = request.GET.get('page')
    pages, page, matches = service.get_matches(contest, request, page)
    result = {'pages': pages, 'page': page, 'data': matches}
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
def do_contest(request):
    data = {}
    if 'id' in request.GET:
        contest = get_object_or_404(Contest, pk=request.GET['id'])
        if 'generate' in request.GET:
            data['success'] = service.generate_match(contest, request.user)
        elif 'submit' in request.GET:
            data['success'] = service.submit_match(request, contest)
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_time_string(time):
    minutes = time / 60
    seconds = time % 60
    min_str = str(minutes)
    sec_str = str(seconds)
    if minutes < 10:
        min_str = '0' + str(minutes)
    if seconds < 10:
        sec_str = '0' + str(seconds)
    return min_str + ':' + sec_str


@login_required
def export_results(request):
    contest = service.get_contest_from_request(request, True)
    matches = Match.objects.filter(
        contestant__in=Contestant.objects.filter(contest=contest, is_deleted=False))
    data = []
    writing_questions = WritingQuestion.objects.filter(contest=contest)
    now = timezone.now()
    for m in matches:
        t = {}
        t[resource. contestant_user_username] = m.contestant.user.username
        t[resource.contestant_user_fullname] = str(m.contestant.user)
        t[resource.contestant_match] = m.match_id
        t[resource.contest_time] = ''
        if not in_range(m.start_time, m.end_time, now):
            t[resource.contest_time] = get_time_string(
                (m.end_time - m.start_time).seconds)
        t[resource.mc_passed_responses] = m.mc_passed_responses
        i = 1
        writing_responses = json.loads(m.writing_responses)
        for q in writing_questions:
            l = '%s %s %s' % (unicode(str(i + 5)),
                              resource.writing, unicode(str(i)))
            if i + 5 < 10:
                l = unicode(str(0)) + l
            if str(q.id) in writing_responses:
                t[l] = writing_responses[str(q.id)]
            else:
                t[l] = ''
            i += 1
        data.append(t)
    return excel.make_response_from_records(data, 'xlsx', file_name='results')


@login_required
def match_detail(request):
    contest = service.get_contest_from_request(request, True)
    match = get_object_or_404(Match, pk=request.GET.get('match_id'))
    data = {}

    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def match_results(request):
    contest = service.get_contest_from_request(request)
    contestants = Contestant.objects.filter(contest=contest, user=request.user)
    if contestants.count() == 0:
        return HttpResponse(json.dumps([]), content_type='application/json')
    matches = Match.objects.filter(contestant=contestants[0])
    result = []
    now = timezone.now()
    for m in matches:
        t = {
            'use_mc_test': contest.use_mc_test,
            'contest_time': (m.end_time - m.start_time).seconds,
            'mc_passed_responses': m.mc_passed_responses,
            'match_name': m.match_id,
            'doing': in_range(m.start_time, m.end_time, now)
        }
        result.append(t)
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
def delete(request):
    contest = service.get_contest_from_request(request, True)
    contest.delete()
    result = {'success': True}
    return HttpResponse(json.dumps(result), content_type='application/json')
