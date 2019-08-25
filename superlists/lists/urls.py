from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^the-only-list-in-the-world/$', views.view_list, name='view_list')
]
