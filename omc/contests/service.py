from datetime import timedelta
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


def get_contest_from_request(request):
    if not request.user.is_superuser and not request.user.can_create_contest:
        raise PermissionDenied
    if not 'id' in request.GET:
        raise Http404
    contest = get_object_or_404(Contest, pk=request.GET['id'])
    if not request.user.is_superuser:
        if not can_manage_contest(contest, request.user):
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
    n = min(contest.mc_test_questions, mc_questions.count())
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
    result = []
    for wq in writing_questions:
        result.append[wq.id]
    return result


def generate_match(contestant):
    matches = Match.objects.filter(contestant=contestant)
    now = timezone.now()
    contest = contestant.contest
    if matches.count() < contest.maximum_of_matches:
        if matches.filter(start_time__lte=now, end_time__gte=now).count() == 0:
            contestant.participated = True
            contestant.save()
            match = Match.objects.create(
                contestant=contestant, match_id=(matches.count() + 1))
            if contest.use_mc_test:
                match.mc_test_questions = json.dumps(
                    generate_mc_questions(contest))
            else:
                match.mc_test_questions = '[]'
            if contest.user_writing_test:
                match.writing_test_questions = json.dumps(
                    generate_writing_questions(contest))
            else:
                match.writing_test_questions = '[]'
            now = timezone.now()
            match.start_time = now
            match.end_time = now + \
                timedelta(minutes=contest.contest_time)
            match.save()
            return True
    return False
