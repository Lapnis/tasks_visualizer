from django.conf.urls import url

from week_scheduler import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_event/', views.add_event_form, name="add_event")
]