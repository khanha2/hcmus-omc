from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from common.utilities import get_paginated_list
from contests.models import Contest, ContestManager


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
        managers = ContestManager.objects.filter(
            contest=contest, user=request.user)
        if managers.count() == 0:
            raise PermissionDenied
    return contest
