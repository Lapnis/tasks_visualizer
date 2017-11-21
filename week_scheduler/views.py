

# Create your views here.
from django.shortcuts import render
from django.http.response import *

from week_scheduler.models import *

import datetime

def index(request):
    return render(request, 'week_scheduler/index.html')


def  add_event_form(request):
    if request.POST:
        post = request.POST
        for w in Week.objects.all():
            print(str(w))

        week = Week.objects.filter(number=int(post['week']), semester=int(post['semester'])).first()
        course = Course.objects.filter(code=post['course']).first()

        event = Event(course=course,
                      name=post['name'],
                      deadline=datetime.datetime.fromtimestamp(int(post['deadline'])),
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