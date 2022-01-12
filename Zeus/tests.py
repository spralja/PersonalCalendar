from django.test import TestCase
from .models import Event, EventManager
from datetime import datetime, timezone, timedelta


UTC = timezone.utc


class EventTestCase(TestCase):
    def test_duration(self):
        event = Event(
            start_time=datetime(2022, 1, 12, 9, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 9, 30, tzinfo=UTC),
            name='Breakfast'
        )

        self.assertEquals(event.duration(), timedelta(minutes=30))


class EventManagerIntervalTestCase(TestCase):
    def setUp(self):
        self.E = Event.objects.create(
            start_time=datetime(2022, 1, 12, 10, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 11, 0, tzinfo=UTC),
            name='Second Breakfast',
        )

    def test__A_B_E1_E2(self):
        start_time = self.E.start_time - 2 * self.E.duration()
        end_time = self.E.start_time - self.E.duration()
        events = Event.objects.interval(start_time, end_time)
        self.assertEquals(len(events), 0)

    def test__A_BE1_E2(self):
        start_time = self.E.start_time - self.E.duration()
        end_time = self.E.start_time
        events = Event.objects.interval(start_time, end_time)
        self.assertEquals(len(events), 0)

    def test__A_E1_B_E2(self):
        start_time = self.E.start_time - self.E.duration()
        end_time = self.E.start_time + self.E.duration() / 2.0
        events = Event.objects.interval(start_time, end_time)
        self.assertEquals(len(events), 1)
    
    def test__A_E1_E2_B(self):
        start_time = self.E.start_time - self.E.duration()
        end_time = self.E.end_time + self.E.duration()
        events = Event.objects.interval(start_time, end_time)
        self.assertEquals(len(events), 1)

    def test__A_E1_E2B(self):
        start_time = self.E.start_time - self.E.duration()
        end_time = self.E.end_time
        events = Event.objects.interval(start_time, end_time)
        self.assertEquals(len(events), 1)

    def test__AE1_B_E2(self):
        start_time = self.E.start_time
        end_time = self.E.start_time + self.E.duration() / 2.0
        events = Event.objects.interval(start_time, end_time)
        self.assertEquals(len(events), 1)

    def test__AE1_E2B(self):
        start_time = self.E.start_time
        end_time = self.E.end_time
        events = Event.objects.interval(start_time, end_time)
        self.assertEquals(len(events), 1)

    def test__E1_A_B_E2(self):
        start_time = self.E.start_time + self.E.duration() / 3
        end_time = self.E.end_time - self.E.duration() / 3
        events = Event.objects.interval(start_time, end_time)
        self.assertEquals(len(events), 1)

    def test__E1_A_E2B(self):
        start_time = self.E.start_time + self.E.duration() / 2
        end_time = self.E.end_time
        events = Event.objects.interval(start_time, end_time)
        self.assertEquals(len(events), 1)

    def test__E1_E2_A_B(self):
        start_time = self.E.end_time + self.E.duration()
        end_time = self.E.end_time + 2 * self.E.duration()
        events = Event.objects.interval(start_time, end_time)
        self.assertEquals(len(events), 0)

    def test__E1_E2A_B(self):
        start_time = self.E.end_time
        end_time = self.E.end_time + self.E.duration()
        events = Event.objects.interval(start_time, end_time)
        self.assertEquals(len(events), 0)

    def test__AB(self):
        start_time = datetime(2022, 1, 12, 10, 0, tzinfo=UTC)
        end_time = start_time = datetime(2022, 1, 12, 10, 0, tzinfo=UTC)
        with self.assertRaises(ValueError):
            events = Event.objects.interval(start_time, end_time)

    def test__B_A(self):
        start_time = datetime(2022, 1, 12, 10, 0, tzinfo=UTC)
        end_time = datetime(2022, 1, 12, 9, 0, tzinfo=UTC)
        with self.assertRaises(ValueError):
            events = Event.objects.interval(start_time, end_time)