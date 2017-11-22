#!/usr/bin/env python
# -- coding: utf-8 --
from django.test import TestCase
from django.test.client import RequestFactory
from week_scheduler.models import *
from week_scheduler.views import *
from datetime import datetime
from pytz import utc



# Create your tests here.
# -----------------------Start: Initial model testing------------------------ #


class WeekModelTestCase(TestCase):
    def event_creator(self, name="Event", load=0, week=None):
        c = Course.objects.create(name="Curso", code="cc6969")
        return Event.objects.create(name=name + str(datetime.now()),
                                    load=load, week=week, type=0, course=c,
                                    deadline=datetime(2017, 11, 25, tzinfo=utc))

    def setUp(self):
        self.w1 = Week.objects.create(number=14, semester=1, since=datetime(2017, 11, 13, tzinfo=utc))
        self.w2 = Week.objects.create(number=15, semester=1, since=datetime(2017, 11, 20, tzinfo=utc))

    def test_week_query_by_since_exact_one(self):
        w = Week.objects.filter(since=datetime(2017, 11, 13, tzinfo=utc)).first()
        self.assertIsNotNone(w)
        self.assertEqual(w.load, 0)

    def test_week_query_lte_exact_two(self):
        w = Week.objects.filter(since__lte=datetime(2017, 11, 20, tzinfo=utc))
        self.assertEqual(w.count(), 2)

    def test_week_query_gte_exact_two(self):
        w = Week.objects.filter(since__gte=datetime(2017, 11, 13, tzinfo=utc))
        self.assertEqual(w.count(), 2)

    def tet_week_query_lt_exact_one(self):
        w = Week.objects.filter(since__lt=datetime(2017, 11, 20, tzinfo=utc))
        self.assertEqual(w.count(), 1)

    def test_week_query_gt_exact_one(self):
        w = Week.objects.filter(since__gt=datetime(2017, 11, 13, tzinfo=utc))
        self.assertEqual(w.count(), 1)

    def test_week_load_per_events(self):
        # arrange
        pesos = [1, 1, 2, 3, 3]
        events = [self.event_creator(load=p, week=self.w1) for p in pesos]
        # act
        week_load = sum(pesos)
        # assert
        self.assertEqual(week_load, self.w1.load)

    def test_week_load_when_event_is_deleted(self):
        # arrange
        pesos = [1, 1, 2, 3, 3]
        events = [self.event_creator(load=p, week=self.w1) for p in pesos]
        # act
        week_load = self.w1.load
        events[-1].delete()
        # assert
        self.assertEqual(week_load - events[-1].load, self.w1.load)

    def test_week_load_when_event_is_moved(self):
        # arrange
        pesos = [1, 1, 2, 3, 3]
        events = [self.event_creator(load=p, week=self.w1) for p in pesos]
        # act
        pre_load_w1 = self.w1.load
        pre_load_w2 = self.w2.load
        events[-1].switch_week(self.w2)
        # assert
        self.assertEqual(events[-1].week, self.w2)
        self.assertEqual(self.w1.load, pre_load_w1 - events[-1].load)
        self.assertEqual(self.w2.load, pre_load_w2 + events[-1].load)


class CourseModelTestCase(TestCase):
    def setUp(self):
        Course.objects.create(code="CC1000", name="Test")

    def test_course_created_correctly(self):
        c1 = Course.objects.filter(code="CC1000").first()
        c2 = Course.objects.filter(name="Test").first()
        self.assertEqual(c1, c2)


class EventModelTestCase(TestCase):
    def setUp(self):
        c = Course.objects.create(code="CC1000", name="Test")
        self.initial_week = Week.objects.create(number=14, semester=1, since=datetime(2017, 11, 13, tzinfo=utc))
        Week.objects.create(number=15, semester=1, since=datetime(2017, 11, 20, tzinfo=utc))
        Event.objects.create(name="Control 1", deadline=datetime(2017, 11, 15, tzinfo=utc), course=c, type=0,
                             week=self.initial_week)

        self.c2 = Course.objects.create(code="CC6402", name="Taller ágilidad y leanpio")

    def test_event_created_properly(self):
        c = Course.objects.filter(code="CC1000").first()
        event = Event.objects.filter(name="Control 1", course=c).first()
        self.assertIsNotNone(event)
        self.assertEqual(event.name, "Control 1")
        self.assertEqual(event.deadline, datetime(2017, 11, 15, tzinfo=utc))
        self.assertEqual(event.type, 0)

    def test_event_initial_week_is_same_as_deadline_week(self):
        event = Event.objects.filter(name="Control 1").first()
        week = Week.objects.filter(since=datetime(2017, 11, 13, tzinfo=utc)).first()

        self.assertEqual(event.week, week)

    def test_event_week_cannot_be_later_than_deadline_week(self):
        # hacer un assertRaise, este test esta hecho para verificar que haya uin ValueError
        event = Event.objects.filter(name="Control 1").first()
        event.week = Week.objects.filter(since=datetime(2017, 11, 20, tzinfo=utc)).first()

        try:
            event.save()
            self.fail("Event object's week cannot be later than deadline's week")
        except ValueError:
            # expected error, test passed
            pass

    def test_event_load_is_between_range(self):
        # arrange
        c = Course.objects.create(code="CC1001", name="Test_2")
        e1 = Event.objects.create(name="1-prior_event", deadline=datetime(2017, 11, 25, tzinfo=utc),
                                  course=c, type=0, load=1, week=self.initial_week)
        e2 = Event.objects.create(name="2-prior_event", deadline=datetime(2017, 11, 25, tzinfo=utc),
                                  course=c, type=0, load=2, week=self.initial_week)
        e3 = Event.objects.create(name="3-prior_event", deadline=datetime(2017, 11, 17, tzinfo=utc),
                                  course=c, type=0, load=3, week=self.initial_week)
        e4 = Event.objects.create(name="4-prior_event", deadline=datetime(2017, 11, 17, tzinfo=utc),
                                  course=c, type=0, load=5, week=self.initial_week)
        e5 = Event.objects.create(name="5-prior_event", deadline=datetime(2017, 11, 17, tzinfo=utc),
                                  course=c, type=0, load=-5, week=self.initial_week)
        # act
        # assert
        self.assertEqual(e4.load, 3, "La tarea se setea a la prioridad mas alta")
        self.assertEqual(e5.load, 1, "La tarea se setea a la prioridad mas baja")
        self.assertEqual(e1.load, 1, "La tarea tiene la prioridad mas baja")
        self.assertEqual(e2.load, 2, "La tarea tiene la prioridad media")
        self.assertEqual(e3.load, 3, "La tarea tiene la prioridad mas alta")

    def test_course_cant_have_events_with_same_name(self):
        try:
            Event.objects.create(name="Control 1", deadline=datetime(2017, 11, 15, tzinfo=utc), course= self.c2, type=0, week=self.initial_week)
            Event.objects.create(name="Control 1", deadline=datetime(2017, 11, 15, tzinfo=utc), course= self.c2, type=0, week=self.initial_week)
            self.fail("Course can't have 2 events with the same name")
        except ValueError:
            pass

    def test_different_courses_can_have_events_with_the_same_name(self):
        c3 = Course.objects.create(code="CC2020", name="test2")
        Event.objects.create(name="Control 1", deadline=datetime(2017, 11, 15, tzinfo=utc), course=self.c2, type=0,
                             week=self.initial_week)
        Event.objects.create(name="Control 1", deadline=datetime(2017, 11, 15, tzinfo=utc), course=c3, type=0,
                             week=self.initial_week)

    def tearDown(self):
        Week.objects.all().delete()
        Course.objects.all().delete()
        Event.objects.all().delete()


class APITestCase(TestCase):
    def setUp(self):
        self.c = Course.objects.create(code="CC6402", name="Taller ágilidad y leanpio")
        self.week = Week.objects.create(number=15, semester=1, since=datetime(2017, 11, 20, tzinfo=utc))
        self.factory = RequestFactory()

    def test_event_form_is_correct(self):
        request = self.factory.post(path='/week_scheduler/add_event/')
        request.POST = {
            'course': 'CC6402',
            'deadline': '1511136020',
            'week': 15,
            'semester': 1,
            'load': 2,
            'type': 0,
            'name': 'Control 3'
        }
        response = add_event_form(request)
        self.assertEqual(response.status_code, 200)

        event = Event.objects.filter(name="Control 3").first()
        self.assertIsNotNone(event)
        self.assertEqual(event.name, "Control 3")
        self.assertEqual(event.load, 2)
        self.assertEqual(event.type, 0)

        self.assertEqual(event.deadline.year, 2017)
        self.assertEqual(event.deadline.month, 11)
        self.assertEqual(event.deadline.day, 20)

        self.assertEqual(self.week, event.week)
        self.assertEqual(self.c, event.course)
