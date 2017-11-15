from django.conf.urls import url

from week_scheduler import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]