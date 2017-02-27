from contests.models import Contest, ContestManager

from common.utilities import get_paginated_list


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
