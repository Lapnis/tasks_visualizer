

# Create your views here.
from django.shortcuts import render
from django.template import RequestContext


def index(request):
    return render(request, 'week_scheduler/index.html')