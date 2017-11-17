from datetime import timedelta

from django.db import models

import pdb

# Create your models here.


class Week(models.Model):
    since = models.DateTimeField(null=False, name="since")
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
    """
    Necessary initial parameters: deadline, name, week
    """
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
        # check if the week to save is no later than deadline's week
        deadline_week = self.deadline - timedelta(days=self.deadline.weekday())  # deadline's first weekday
        if self.week.since > Week.objects.filter(since=deadline_week).first().since:
            raise ValueError
        self.week.load += self.load

    def save(self, *args, **kwargs):
        self.check_load()
        self.pre_save_handler()
        super(Event, self).save(*args, **kwargs)

    def check_load(self):
        """ Verifica los correctos valores de la carga de un evento [1,2,3] o los ajusta """
        if self.load > 3:
            self.load = 3
        elif self.load < 1:
            self.load = 1

    def delete(self):
        self.week.load -= self.load
        super(Event, self).delete()

    def switch_week(self, new_week):
        self.week.load -= self.load
        self.week = new_week
        self.week.load += self.load
