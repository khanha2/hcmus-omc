from django.conf.urls import url

from contests import views

urlpatterns = [
    url(r'^contests/$', views.contests, name='contests'),
    url(r'^create/$', views.create, name='create'),
    url(r'^update/$', views.update, name='update'),
]
