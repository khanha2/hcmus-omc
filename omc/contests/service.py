from datetime import timedelta
import json
import random

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone

from common.utilities import get_paginated_list
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
        if not c.from_time or not c.to_time:
            contest_dict['time_string'] = None
        else:
            contest_dict[
                'time_string'] = '%s - %s' % (str(c.from_time), str(c.to_time))
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
            v = random.randint(0, mc_questions.count() - 1)
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
    contest = contestant.contest
    if matches.count() < contest.maximum_of_matches:
        if matches.filter(start_time__lte=now, end_time__gte=now).count() == 0:
            contestant.participated = True
            contestant.save()
            match = Match.objects.create(
                contestant=contestant, match_id=(matches.count() + 1))
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


def load_mc_questions(match):
    mc_question_ids = json.loads(match.mc_questions)
    result = []
    view_id = 1
    for i in mc_question_ids:
        question = MCQuestion.objects.get(id=i)
        result.append({
            'id': question.id,
            'view_id': view_id,
            'content': question.content,
            'a': question.a,
            'b': question.b,
            'c': question.c,
            'd': question.d,
        })
        view_id += 1
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
                        if value == question.answer:
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
