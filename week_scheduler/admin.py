from django.contrib import admin

from .models import Week, Course, Event
# Register your models here.

admin.site.register(Week)
admin.site.register(Course)
admin.site.register(Event)
