from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^change-password/$', views.change_password, name='change_password')
]
