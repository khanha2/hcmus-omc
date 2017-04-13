from datetime import timedelta
import json
import random

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from common.utilities import get_paginated_list, in_range
from contests.models import Contest, ContestManager, Contestant, MCQuestion, WritingQuestion, Match


def contests(search_criteria=None):
    if search_criteria and 'management' in search_criteria and 'user' in search_criteria:
        contest_objects = [cm.contest for cm in ContestManager.objects.filter(
            user=search_criteria['user'], is_deleted=False)]
    else:
        contest_objects = Contest.objects.filter(is_deleted=False)
    contest_objects = contest_objects.order_by('-from_time')
    result = []
    for c in contest_objects:
        contest_dict = {}
        contest_dict['id'] = c.id
        contest_dict['name'] = c.name
        contest_dict['short_description'] = c.short_description
        if not c.from_time or not c.to_time:
            contest_dict['time_string'] = None
        else:
            contest_dict[
                'time_string'] = '%s - %s' % (c.from_time.strftime('%m/%d/%Y %I:%M %p'), c.to_time.strftime('%m/%d/%Y %I:%M %p'))
        result.append(contest_dict)
    return result


def get_contest_from_request(request, management=False):
    if not 'id' in request.GET:
        raise Http404
    contest = get_object_or_404(Contest, pk=request.GET['id'])
    if contest.is_deleted:
        raise Http404
    if management and not can_manage_contest(contest, request.user):
        raise PermissionDenied
    return contest


def can_participate_contest(contest):
    now = timezone.now()
    if not contest.from_time or not contest.to_time:
        return False
    if now < contest.from_time or now > contest.to_time:
        return False
    return True


def can_manage_contest(contest, user):
    if not user.id:
        return False
    if user.is_superuser:
        return True
    managers = ContestManager.objects.filter(contest=contest, user=user)
    return managers.count() > 0


def remaining_matches(contest, user):
    contestant = Contestant.objects.filter(contest=contest, user=user)
    if contestant.count() == 0:
        return contest.maximum_of_matches
    remaining_matches = contest.maximum_of_matches - \
        Match.objects.filter(contestant=contestant).count()
    return remaining_matches if remaining_matches > 0 else 0


def generate_mc_questions(contest):
    choosed = {}
    result = []
    mc_questions = MCQuestion.objects.filter(contest=contest)
    n = min(contest.mc_questions, mc_questions.count())
    for i in range(n):
        p = random.randint(0, mc_questions.count() - 1)
        question_id = mc_questions[p].id
        while question_id in choosed:
            p = random.randint(0, mc_questions.count() - 1)
            question_id = mc_questions[p].id
        result.append(question_id)
        choosed[question_id] = ''
    return result


def generate_writing_questions(contest):
    writing_questions = WritingQuestion.objects.filter(contest=contest)
    result = [wq.id for wq in writing_questions]
    return result


def generate_match(contest, user):
    contestant, _ = Contestant.objects.get_or_create(
        contest=contest, user=user)
    matches = Match.objects.filter(contestant=contestant, is_deleted=False)
    now = timezone.now()
    count = matches.count()
    if count < contest.maximum_of_matches:
        if matches.filter(start_time__lte=now, end_time__gte=now).count() == 0:
            match = Match(contestant=contestant, match_id=(count + 1))
            if contest.use_mc_test:
                match.mc_questions = json.dumps(generate_mc_questions(contest))
            else:
                match.mc_questions = '[]'
            if contest.use_writing_test:
                match.writing_questions = json.dumps(
                    generate_writing_questions(contest))
            else:
                match.writing_questions = '[]'
            now = timezone.now()
            match.start_time = now
            match.end_time = now + \
                timedelta(minutes=contest.contest_time)
            match.save()
        return True
    return False


def load_mc_questions(match, get_answers=False):
    mc_question_ids = json.loads(match.mc_questions)
    result = []
    view_id = 1
    for i in mc_question_ids:
        try:
            question = MCQuestion.objects.get(id=i)
            d = {'id': question.id, 'view_id': view_id, 'content': question.content,
                 'a': question.a, 'b': question.b, 'c': question.c, 'd': question.d}
            if get_answers:
                d['answer'] = question.answer
            result.append(d)
            view_id += 1
        except:
            pass
    return result


def load_writing_questions(match):
    writing_question_ids = json.loads(match.writing_questions)
    result = []
    view_id = 1
    for i in writing_question_ids:
        question = WritingQuestion.objects.get(id=i)
        result.append({
            'id': question.id,
            'view_id': view_id,
            'content': question.content,
        })
        view_id += 1
    return result


def get_current_match(contestant):
    now = timezone.now()
    success = False
    match = Match.objects.filter(
        contestant=contestant, start_time__lte=now, end_time__gte=now, is_deleted=False)
    data = {}
    if match.exists():
        contest = contestant.contest
        match = match[0]
        data['remaining'] = (match.end_time - now).seconds
        if contest.use_mc_test:
            data['mc_questions'] = load_mc_questions(match)
        if contest.use_writing_test:
            data['writing_questions'] = load_writing_questions(match)
        return data
    return None


def submit_match(request, contest):
    data = {}
    if request.method == 'POST':
        now = timezone.now()
        contestant = Contestant.objects.filter(
            contest=contest, user=request.user, is_deleted=False)
        match = Match.objects.filter(
            contestant=contestant, start_time__lte=now, end_time__gte=now, is_deleted=False)
        if match.exists():
            match = match[0]
            if now - match.end_time <= timedelta(seconds=30):
                if now < match.end_time:
                    match.end_time = now
                    match.save()
                mc_question_ids = json.loads(match.mc_questions)
                passed_questions = 0
                mc_responses = {}
                for i in mc_question_ids:
                    question = MCQuestion.objects.get(id=i)
                    param_name = 'mcr_' + str(i)
                    if param_name in request.POST:
                        value = request.POST[param_name].strip()
                        mc_responses[i] = value
                        if value.upper() == question.answer.upper():
                            passed_questions += 1
                match.mc_responses = json.dumps(mc_responses)
                match.mc_passed_responses = passed_questions
                writing_questions_ids = json.loads(match.writing_questions)
                writing_responses = {}
                for i in writing_questions_ids:
                    param_name = 'wtr_' + str(i)
                    if param_name in request.POST:
                        writing_responses[str(i)] = request.POST[param_name]
                match.writing_responses = json.dumps(writing_responses)
                match.save()
                return True
    return False


def get_matches(contest, search_criteria=None, page=1):
    pages, page, matches = get_paginated_list(Match.objects.filter(
        contestant__in=Contestant.objects.filter(contest=contest)), page)
    result = []
    now = timezone.now()
    for match in matches:
        result.append({
            'user_id': match.contestant.user.id,
            'user_username': match.contestant.user.username,
            'user_fullname': str(match.contestant.user),
            'contest_id': match.contestant.contest.id,
            'match_id': match.id,
            'match_name': match.match_id,
            'use_mc_test': match.contestant.contest.use_mc_test,
            'use_writing_test': match.contestant.contest.use_writing_test,
            'mc_passed_responses': match.mc_passed_responses,
            'contest_time': (match.end_time - match.start_time).seconds,
            'doing': in_range(match.start_time, match.end_time, now)
        })
    return pages, page, result


def get_match_detail(match):
    data = {
        'user_fullname': str(match.contestant.user),
        'use_mc_test': match.contestant.contest.use_mc_test,
        'use_writing_test': match.contestant.contest.use_writing_test,
    }
    contest = match.contestant.contest
    if contest.use_mc_test:
        mc_question_ids = json.loads(match.mc_questions)
        mc_questions = MCQuestion.objects.filter(id__in=mc_question_ids)
        mc_responses = json.loads(match.mc_responses)
        temp_data = []
        for q in mc_questions:
            t = {'id': q.id,
                 'content': q.content,
                 'answer': q.answer}
            if q.id in mc_responses:
                t['response'] = mc_responses['q.id']
            temp_data.append(t)
        data['mc_questions'] = temp_data
    if contest.use_writing_test:
        writing_question_ids = json.loads(match.writing_questions)
        writing_questions = WritingQuestion.objects.filter(
            id__in=writing_question_ids)
        writing_responses = json.loads(match.writing_responses)
        temp_data = []
        for q in writing_questions:
            t = {'id': q.id,
                 'content': q.content}
            if q.id in writing_responses:
                t['response'] = writing_responses['q.id']
            temp_data.append(t)
        data['writing_questions'] = temp_data
    return data
