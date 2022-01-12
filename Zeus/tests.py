from django.test import TestCase
from .models import Event, EventManager
from datetime import datetime, timezone, timedelta


UTC = timezone.utc


class EventTestCase(TestCase):
    def test_duration(self):
        event = Event(
            start_time=datetime(2022, 1, 12, 9, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 10, 0, tzinfo=UTC),
            name='Breakfast'
        )

        self.assertEquals(event.duration(), timedelta(hours=1))

    
    # ordering tests

    # E1 = E.start_time
    # E2 = E.end_time
    # F1 = F.start_time
    # F2 = F.end_time

    def test__E1_E2_F1_f2(self):
        E = Event.objects.create(
            start_time=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            name='Dinner',
        )

        F = Event.objects.create(
            start_time=datetime(2022, 1, 12, 22, 0, tzinfo=UTC),
            end_time = datetime(2022, 1, 13, 23, 0, tzinfo=UTC),
            name='Second Dinner'
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1_E2F1_F2(self):
        E = Event.objects.create(
            start_time=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            name='Dinner',
        )

        F = Event.objects.create(
            start_time=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            end_time = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            name='Second Dinner'
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1_F1_E2_F2(self):
        E = Event.objects.create(
            start_time=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 22, 0, tzinfo=UTC),
            name='Dinner',
        )

        F = Event.objects.create(
            start_time=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            end_time = datetime(2022, 1, 13, 23, 0, tzinfo=UTC),
            name='Second Dinner'
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1_F1_E2F2(self):
        E = Event.objects.create(
            start_time=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 22, 0, tzinfo=UTC),
            name='Dinner',
        )

        F = Event.objects.create(
            start_time=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            end_time = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            name='Second Dinner'
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1F1_E2_F2(self):
        E = Event.objects.create(
            start_time=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            name='Dinner',
        )

        F = Event.objects.create(
            start_time=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            end_time = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            name='Second Dinner'
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1F1_E2F2(self):
        # this does not as off yet have a test case it should come here in the future when the behaviour is defined
        pass

    def test__F1_E1_E2_F2(self):
        E = Event.objects.create(
            start_time=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            name='Dinner',
        )

        F = Event.objects.create(
            start_time=datetime(2022, 1, 12, 19, 0, tzinfo=UTC),
            end_time = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            name='Second Dinner'
        )

        events = Event.objects.all()
        self.assertEquals(events[0], F)
        self.assertEquals(events[1], E)

        events.delete()

    def test__F1_E1_E2F2(self):
        E = Event.objects.create(
            start_time=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            name='Dinner',
        )

        F = Event.objects.create(
            start_time=datetime(2022, 1, 12, 19, 0, tzinfo=UTC),
            end_time = datetime(2022, 1, 13, 21, 0, tzinfo=UTC),
            name='Second Dinner'
        )

        events = Event.objects.all()
        self.assertEquals(events[0], F)
        self.assertEquals(events[1], E)

        events.delete()

    def test__F1E1_E2_F2(self):
        E = Event.objects.create(
            start_time=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            name='Dinner',
        )

        F = Event.objects.create(
            start_time=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            end_time = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            name='Second Dinner'
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()


class EventManagerIntervalTestCase(TestCase):
    def setUp(self):
        self.E = Event.objects.create(
            start_time=datetime(2022, 1, 12, 10, 0, tzinfo=UTC),
            end_time=datetime(2022, 1, 12, 11, 0, tzinfo=UTC),
            name='Second Breakfast',
        )

    # A = start_time
    # B = end_time
    # E1 = E.start_time
    # E2 = E.end_time


    # tests with start_time and end_timed
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


    # tests with start_time only
    def test__A_E1_E2(self):
        start_time = self.E.start_time - self.E.duration()
        events = Event.objects.interval(start_time=start_time)
        self.assertEquals(len(events), 1)

    def test__AE1_E2(self):
        start_time = self.E.start_time
        events = Event.objects.interval(start_time=start_time)
        self.assertEquals(len(events), 1)

    def test__E1_A_E2(self):
        start_time = self.E.start_time + self.E.duration() / 2 
        events = Event.objects.interval(start_time=start_time)
        self.assertEquals(len(events), 1)

    def test__E1_E2A(self):
        start_time = self.E.end_time
        events = Event.objects.interval(start_time=start_time)
        self.assertEquals(len(events), 0)

    def test__E1_E2_A(self):
        start_time = self.E.end_time + self.E.duration()
        events = Event.objects.interval(start_time=start_time)
        self.assertEquals(len(events), 0)


    # tests with end_time only
    def test__B_E1_E2(self):
        end_time = self.E.start_time - self.E.duration()
        events = Event.objects.interval(end_time=end_time)
        self.assertEquals(len(events), 0)

    def test__BE1_E2(self):
        end_time = self.E.start_time
        events = Event.objects.interval(end_time=end_time)
        self.assertEquals(len(events), 0)

    def test__E1_B_E2(self):
        end_time = self.E.start_time + self.E.duration() / 2
        events = Event.objects.interval(end_time=end_time)
        self.assertEquals(len(events), 1)

    def test__E1_E2B(self):
        end_time = self.E.end_time
        events = Event.objects.interval(end_time=end_time)
        self.assertEquals(len(events), 1)

    def test__E1_E2_B(self):
        end_time = self.E.end_time + self.E.duration()
        events = Event.objects.interval(end_time=end_time)
        self.assertEquals(len(events), 1)


    # test with empty interval
    def test_E1_E2(self):
        events = Event.objects.interval()
        self.assertEquals(len(events), 1)
    

    # ValueError exception tests
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
