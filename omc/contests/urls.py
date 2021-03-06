from django.conf.urls import url

from contests import views

urlpatterns = [
    url(r'^contests/$', views.contests, name='contests'),
    url(r'^create/$', views.create, name='create'),
    url(r'^update/$', views.update, name='update'),
    url(r'^upload-questions/$', views.upload_questions, name='upload_questions'),
    url(r'^questions/$', views.questions, name='questions'),
    url(r'^do-contest/$', views.do_contest, name='do_contest'),
    url(r'^contestants/$', views.contestants, name='contestants'),
    url(r'^export-results/$', views.export_results, name='export_results'),
    url(r'^match-detail/$', views.match_detail, name='match_detail'),
    url(r'^match-results/$', views.match_results, name='match_results')
]
