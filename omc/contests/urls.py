from django.conf.urls import url

from contests import views

urlpatterns = [
    url(r'^contests/$', views.contests, name='contests'),
    url(r'^create/$', views.create, name='create'),
    url(r'^update/$', views.update, name='update'),
    url(r'^upload-questions/$', views.upload_questions, name='upload_questions'),
    url(r'^upload-questions/writings/$', views.upload_writing_test_questions, name='upload_writing_test_questions')
]
