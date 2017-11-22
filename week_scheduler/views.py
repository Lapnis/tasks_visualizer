

# Create your views here.
from django.shortcuts import render
from django.http.response import *

from week_scheduler.models import *

import datetime

def index(request):
    courses = Course.objects.all()
    weeks = Week.objects.all()
    myContext = {'courses': courses, 'weeks': weeks}
    return render(request, 'week_scheduler/index.html', context=myContext)


def  add_event_form(request):
    if request.POST:
        post = request.POST
        for w in Week.objects.all():
            print(str(w))

        week = Week.objects.filter(id=int(post['week'])).first()
        course = Course.objects.filter(id=post['course']).first()

        event = Event(course=course,
                      name=post['name'],
                      deadline= datetime.datetime.strptime(post['deadline'], "%d/%m/%Y"),
                      week=week,
                      load=int(post['load']),
                      type=int(post['type']))
        try:
            event.save()
            return HttpResponse(status=200)
        except ValueError as e:
            return HttpResponseBadRequest({'Save error: ' + e.__str__()})

    else:
        return HttpResponseBadRequest({'POST method'})