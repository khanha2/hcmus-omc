from django.conf.urls import url

from webapp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^contest/$', views.contest_overview, name='contest_overview'),
    url(r'^contest/do-contest/$', views.contest_do_contest, name='contest_do_contest'),
    url(r'^contest/admin/$', views.contest_admin, name='contest_admin'),
    url(r'^user/$', views.user, name='user'),
    url(r'^contests/$', views.contests, name='contests'),
]
