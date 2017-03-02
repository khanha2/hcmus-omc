from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone

from common.utilities import get_paginated_list
from contests.models import Contest, ContestManager, Contestant, Match


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
