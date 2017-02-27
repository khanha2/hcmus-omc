from django.conf.urls import url

from webapp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^contest/$', views.contest_overview, name='contest_overview'),
    url(r'^contest/mc-test/$', views.contest_mc_test, name='contest_mc_test'),
    url(r'^contest/writing-test/$', views.contest_writing_test,
        name='contest_writing_test'),
    url(r'^contest/admin/$', views.contest_admin, name='contest_admin'),
    url(r'^user/$', views.user, name='user'),
    url(r'^contests/$', views.contests_management, name='contests_management'),
]
