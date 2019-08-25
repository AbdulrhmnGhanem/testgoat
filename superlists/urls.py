from django.conf.urls import url, include
from django.contrib import admin
from superlists.lists import views as list_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', list_views.homepage, name='home'),
    url(r'^lists/', include('superlists.lists.urls', namespace='lists'),),
]
