from contests.models import Contest, ContestManager

from common.utilities import get_paginated_list


def contests(search_criteria=None):
    if search_criteria and 'management' in search_criteria and 'user' in search_criteria:
        contest_objects = [cm.contest for cm in ContestManager.objects.filter(
            user=search_criteria['user'])]
    else:
        contest_objects = Contest.objects.all()
    contest_objects = contest_objects.order_by('-from_time')
    result = []
    for c in contest_objects:
        contest_dict = {}
        contest_dict['id'] = c.id
        contest_dict['name'] = c.name
        contest_dict['from_time'] = str(c.from_time)
        contest_dict['to_time'] = str(c.to_time)
        result.append(contest_dict)
    return result
