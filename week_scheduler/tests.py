from django.test import TestCase
from week_scheduler.models import *
from datetime import datetime
from pytz import utc

# Create your tests here.
# -----------------------Start: Initial model testing------------------------ #


class WeekModelTestCase(TestCase):

    def setUp(self):
        Week.objects.create(since=datetime(2017, 11, 13))
        Week.objects.create(since=datetime(2017, 11, 20))

    def test_week_query_by_since_exact_one(self):
        w = Week.objects.filter(since=datetime(2017, 11, 13)).first()
        self.assertIsNotNone(w)
        self.assertEqual(w.load, 0)

    def test_week_query_lte_exact_two(self):
        w = Week.objects.filter(since__lte=datetime(2017, 11, 20))
        self.assertEqual(w.count(), 2)

    def test_week_query_gte_exact_two(self):
        w = Week.objects.filter(since__gte=datetime(2017, 11, 13))
        self.assertEqual(w.count(), 2)

    def tet_week_query_lt_exact_one(self):
        w = Week.objects.filter(since__lt=datetime(2017, 11, 20))
        self.assertEqual(w.count(), 1)

    def test_week_query_gt_exact_one(self):
        w = Week.objects.filter(since__gt=datetime(2017, 11, 13))
        self.assertEqual(w.count(), 1)


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
        Week.objects.create(since=datetime(2017, 11, 13))
        Week.objects.create(since=datetime(2017, 11, 20))
        Event.objects.create(name="Control 1", deadline=datetime(2017, 11, 15), course=c, type=0)

    def test_event_created_properly(self):
        c = Course.objects.filter(code="CC1000").first()
        event = Event.objects.filter(name="Control 1", course=c).first()
        self.assertIsNotNone(event)
        self.assertEqual(event.name, "Control 1")
        self.assertEqual(event.deadline, datetime(2017, 11, 15, tzinfo=utc))
        self.assertEqual(event.type, 0)

    def test_event_initial_week_is_same_as_deadline_week(self):
        event = Event.objects.filter(name="Control 1").first()
        week = Week.objects.filter(since=datetime(2017, 11, 13)).first()

        self.assertEqual(event.week, week)

    def test_event_week_cannot_be_later_than_deadline_week(self):
        event = Event.objects.filter(name="Control 1").first()
        event.week = Week.objects.filter(since=datetime(2017, 11, 20)).first()

        try:
            event.save()
            self.fail("Event object's week cannot be later than deadline's week")
        except ValueError:
            pass
