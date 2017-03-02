import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

import django_excel as excel
import pyexcel.ext.xls
import pyexcel.ext.xlsx

from common.forms import UploadFileForm
from common.utilities import convert_string_to_time
from contests.models import Contest, ContestManager, MCTestQuestion
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
    contest = service.get_contest_from_request(request)
    if request.method == 'POST':
        for f in Contest.get_field_list():
            if f in request.POST:
                try:
                    if f == 'from_time' or f == 'to_time':
                        update_time(contest, f, request.POST[f])
                    if f == 'use_mc_test' or f == 'use_writing_test':
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

            MCTestQuestion.objects.filter(contest=contest).delete()
            # request.FILES['file'].save_book_to_database(
            # models=[(MCTestQuestion, ['content', 'a', 'b', 'c', 'd',
            # 'answer'], mc_func, 0)])

            sheet = request.FILES['file'].get_sheet().get_array()
            print type(sheet)
            for row in sheet[1:]:
                print row
                question = MCTestQuestion(contest=contest, content=row[0], a=row[
                                          1], b=row[2], c=row[3], d=row[4], answer=row[5])
                question.save()

            # return excel.make_response(request.FILES['file'].get_sheet(),
            # "csv", file_name="download")
    result = {'success': True}
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
def upload_writing_test_questions(request):
    pass


@login_required
def delete_contest(request):
    pass
