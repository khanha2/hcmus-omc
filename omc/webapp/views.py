from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse

from contests.models import Contest, Contestant
from contests import service


def index(request):
    return render(request, 'index.html', {})


def login(request):
    if request.user.id:
        if 'next' in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        return HttpResponseRedirect(reverse('webapp:index'))
    return render(request, 'login.html', {})


@login_required
def logout(request):
    user_logout(request)
    return HttpResponseRedirect(reverse('webapp:index'))


def contest_overview(request):
    contest = service.get_contest_from_request(request)
    if not contest.from_time or not contest.to_time:
        contest.time_string = None
    else:
        contest.time_string = '%s - %s' % (contest.from_time.strftime(
            '%m/%d/%Y %I:%M %p'), contest.to_time.strftime('%m/%d/%Y %I:%M %p'))
    template_data = {'contest': contest,
                     'can_participate': service.can_participate_contest(contest),
                     'can_manage': service.can_manage_contest(contest, request.user)}
    if request.user.id:
        template_data['remaining_matches'] = service.remaining_matches(
            contest, request.user)
    return render(request, 'contests/overview.html', template_data)


@login_required
def contest_do_contest(request):
    contest = service.get_contest_from_request(request)
    contestants = Contestant.objects.filter(contest=contest, user=request.user)
    if contestants.count() == 0:
        raise PermissionDenied
    data = service.get_current_match(contestants[0])
    if data is None:
        raise PermissionDenied
    data['contest'] = contest
    return render(request, 'contests/do_contest.html', data)


@login_required
def contest_admin(request):
    contest = service.get_contest_from_request(request, True)
    return render(request, 'contests/admin/admin.html', {'contest': contest})


@login_required
def contests(request):
    if not request.user.is_superuser and not request.user.can_create_contest:
        raise Http404
    return render(request, 'contests/contests.html', {})


@login_required
def user(request):
    return render(request, 'users/user.html', {})


@login_required
def change_password(request):
    return render(request, 'change_password.html', {})
