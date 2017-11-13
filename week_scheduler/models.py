from datetime import timedelta

from django.db import models

# Create your models here.


class Week(models.Model):
    since = models.DateField(null=False, name="since")
    load = models.IntegerField(null=True, blank=False, default=0, name="load")

    def __str__(self):
        return "week of " + self.since.strftime("%d/%-m/%Y")

    class Meta:
        verbose_name = "semana"
        verbose_name_plural = "semanas"


class Course(models.Model):
    code = models.CharField(max_length=10, null=False, blank=False, name="code")
    name = models.CharField(max_length=128, null=False, blank=False, name="name")

    def __str__(self):
        return self.code + " : " + self.name

    class Meta:
        verbose_name = "curso"
        verbose_name_plural = "cursos"

    def __eq__(self, other):
        return self.code == other.code and self.name == other.name


class Event(models.Model):
    TYPES = ((0, 'test'),
             (1, 'homework'))

    name = models.CharField(max_length=128, null=False, blank=False, name="name")
    deadline = models.DateTimeField(null=False, name="deadline")
    load = models.IntegerField(default=0, name="load")
    week = models.ForeignKey('Week', null=False, blank=False, name="week")
    course = models.ForeignKey('Course', null=False, blank=False, name="course")
    type = models.IntegerField(choices=TYPES, null=False)

    def __str__(self):
        return str(self.course) + " - " + self.name

    class Meta:
        verbose_name = "evento"
        verbose_name_plural = "eventos"

    def pre_save_handler(self):
        deadline_week = self.deadline - timedelta(days=self.deadline.weekday())
        if self.pk:
            # already created, check if the week to save is no later than deadline's week
            if self.week.since > Week.objects.filter(since=deadline_week).first().since:
                raise ValueError
        else:
            # just created, we set te initial week according to deadline's week
            week = Week.objects.filter(since=deadline_week.date()).first()
            if week is None:
                raise ValueError
            self.week = week

    def save(self, *args, **kwargs):
        self.pre_save_handler()
        super(Event, self).save(*args, **kwargs)
