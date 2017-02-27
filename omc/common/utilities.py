from datetime import datetime

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_paginated_list(list, page):
    paginator = Paginator(list, settings.PAGINATE_LIST_BY)
    try:
        listing = paginator.page(page)
    except PageNotAnInteger:
        listing = paginator.page(1)
    except EmptyPage:
        listing = paginator.page(paginator.num_pages)
    return listing


def convert_string_to_date(string):
    try:
        return datetime.strptime(string, '%d/%m/%Y').date()
    except Exception:
        pass
    return None


def convert_string_to_time(string):
    try:
        return datetime.strptime(string, '%d/%m/%Y - %H:%M')
    except Exception:
        pass
    return None
