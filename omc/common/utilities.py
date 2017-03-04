from datetime import datetime

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_paginated_list(list, page=None, paginate_by=settings.PAGINATE_LIST_BY):
    paginator = Paginator(list, paginate_by)
    try:
        listing = paginator.page(page)
    except PageNotAnInteger:
        listing = paginator.page(1)
        page = 1
    except EmptyPage:
        listing = paginator.page(paginator.num_pages)
        page = 1
    return paginator.num_pages, page, listing


def convert_string_to_date(string):
    try:
        return datetime.strptime(string, '%d/%m/%Y').date()
    except Exception:
        pass
    return None


def convert_string_to_time(string):
    try:
        return datetime.strptime(string, '%d/%m/%Y %H:%M')
    except Exception:
        pass
    return None


def in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
