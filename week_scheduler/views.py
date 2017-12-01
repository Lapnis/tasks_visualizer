# Create your views here.
from django.shortcuts import render
from django.http.response import *

from week_scheduler.models import *

import datetime


def index(request):
    courses = Course.objects.all()
    weeks = Week.objects.all().order_by('number')
    events = Event.objects.all()
    myContext = {'courses': courses, 'weeks': weeks, 'events': events}
    return render(request, 'week_scheduler/index.html', context=myContext)

def change_event_week(request):
    if request.POST:
        post = request.POST

        event = Event.objects.get(id=int(post['eventId']))
        week = Week.objects.get(id=int(post['newWeek']))

        try:
            event.switch_week(week)
            return HttpResponse(status=200)
        except ValueError as e:
            return HttpResponseBadRequest({'Save error: ' + e.__str__()})
        except Exception as e:
            return HttpResponseBadRequest({'Unexpected error: ' + e.__str__()})

    else:
        return HttpResponseBadRequest({'POST method'})


def add_event_form(request):
    """ Creates Event object from data given in frontend and returns response """
    if request.POST:
        post = request.POST

        week = Week.objects.filter(number=int(post['week'])).first()
        course = Course.objects.filter(code=post['course']).first()

        event = Event(course=course,
                      name=post['name'],
                      deadline=datetime.datetime.strptime(post['deadline'], "%d/%m/%Y"),
                      week=week,
                      load=int(post['load']),
                      type=int(post['type']))
        try:
            event.save()
            return HttpResponse(status=200)
        except ValueError as e:
            return HttpResponseBadRequest({'Save error: ' + e.__str__()})
        except Exception as e:
            return HttpResponseBadRequest({'Unexpected error: ' + e.__str__()})

    else:
        return HttpResponseBadRequest({'POST method'})
