from django.conf.urls import url, include
from django.contrib import admin
from lists import views as list_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', list_views.homepage, name='home')
]
