from django.test import TestCase
from .models import Calendar, Event, EventManager
from datetime import datetime, timezone, timedelta
import icalendar


UTC = timezone.utc



class EventTestCase(TestCase):
    def setUp(self):
        self.CAL = Calendar.objects.create(name='dummy')

    def test_duration(self):
        event = Event(
            DTSTART=datetime(2022, 1, 12, 9, 0, tzinfo=UTC),
            DTEND=datetime(2022, 1, 12, 10, 0, tzinfo=UTC),
            SUMMARY='Breakfast',
            calendar=self.CAL,
        )

        self.assertEquals(event.duration(), timedelta(hours=1))

    
    # ordering tests

    # E1 = E.DTSTART
    # E2 = E.DTEND
    # F1 = F.DTSTART
    # F2 = F.DTEND

    def test__E1_E2_F1_f2(self):
        E = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            DTEND=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            SUMMARY='Dinner',
            calendar=self.CAL,
        )

        F = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 22, 0, tzinfo=UTC),
            DTEND = datetime(2022, 1, 13, 23, 0, tzinfo=UTC),
            SUMMARY='Second Dinner',
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1_E2F1_F2(self):
        E = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            DTEND=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            SUMMARY='Dinner',
            calendar=self.CAL,
        )

        F = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            DTEND = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            SUMMARY='Second Dinner',
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1_F1_E2_F2(self):
        E = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            DTEND=datetime(2022, 1, 12, 22, 0, tzinfo=UTC),
            SUMMARY='Dinner',
            calendar=self.CAL,
        )

        F = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            DTEND = datetime(2022, 1, 13, 23, 0, tzinfo=UTC),
            SUMMARY='Second Dinner',
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1_F1_E2F2(self):
        E = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            DTEND=datetime(2022, 1, 12, 22, 0, tzinfo=UTC),
            SUMMARY='Dinner',
            calendar=self.CAL,
        )

        F = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            DTEND = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            SUMMARY='Second Dinner',
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1F1_E2_F2(self):
        E = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            DTEND=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            SUMMARY='Dinner',
            calendar=self.CAL,
        )

        F = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            DTEND = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            SUMMARY='Second Dinner',
            calendar=self.CAL,
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
            DTSTART=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            DTEND=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            SUMMARY='Dinner',
            calendar=self.CAL,
        )

        F = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 19, 0, tzinfo=UTC),
            DTEND = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            SUMMARY='Second Dinner',
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], F)
        self.assertEquals(events[1], E)

        events.delete()

    def test__F1_E1_E2F2(self):
        E = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            DTEND=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            SUMMARY='Dinner',
            calendar=self.CAL,
        )

        F = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 19, 0, tzinfo=UTC),
            DTEND = datetime(2022, 1, 13, 21, 0, tzinfo=UTC),
            SUMMARY='Second Dinner',
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], F)
        self.assertEquals(events[1], E)

        events.delete()

    def test__F1E1_E2_F2(self):
        E = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            DTEND=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            SUMMARY='Dinner',
            calendar=self.CAL,
        )

        F = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            DTEND = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            SUMMARY='Second Dinner',
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()


class EventManagerTestCase(TestCase):
    def setUp(self):
        self.CAL = Calendar.objects.create(name='dummy')

    def test_create_raises_validation_error_T2_T1(self):
        DTSTART = datetime(2022, 1, 15, 16, 6, tzinfo=UTC)
        DTEND = datetime(2022, 1, 15, 16, 5, tzinfo=UTC)
        with self.assertRaises(ValueError):
            Event.objects.create(
                DTSTART=DTSTART,
                DTEND=DTEND,
                SUMMARY='dummy',
                calendar=self.CAL,
            )

            Event.objects.delete()

    def test_create_raises_validation_error_T1T2(self):
        DTSTART = datetime(2022, 1, 15, 16, 6, tzinfo=UTC)
        DTEND = datetime(2022, 1, 15, 16, 6, tzinfo=UTC)
        with self.assertRaises(ValueError):
            Event.objects.create(
                DTSTART=DTSTART,
                DTEND=DTEND,
                SUMMARY='dummy',
                cal=self.CAL,
            )

            Event.objects.delete()


class EventManagerIntervalTestCase(TestCase):
    def setUp(self):
        self.CAL = Calendar.objects.create(name='dummy')

        self.E = Event.objects.create(
            DTSTART=datetime(2022, 1, 12, 10, 0, tzinfo=UTC),
            DTEND=datetime(2022, 1, 12, 11, 0, tzinfo=UTC),
            SUMMARY='Second Breakfast',
            calendar=self.CAL,
        )

    # A = DTSTART
    # B = DTEND
    # E1 = E.DTSTART
    # E2 = E.DTEND


    # tests with DTSTART and DTENDd
    def test__A_B_E1_E2(self):
        DTSTART = self.E.DTSTART - 2 * self.E.duration()
        DTEND = self.E.DTSTART - self.E.duration()
        events = Event.objects.interval(DTSTART, DTEND)
        self.assertEquals(len(events), 0)

    def test__A_BE1_E2(self):
        DTSTART = self.E.DTSTART - self.E.duration()
        DTEND = self.E.DTSTART
        events = Event.objects.interval(DTSTART, DTEND)
        self.assertEquals(len(events), 0)

    def test__A_E1_B_E2(self):
        DTSTART = self.E.DTSTART - self.E.duration()
        DTEND = self.E.DTSTART + self.E.duration() / 2.0
        events = Event.objects.interval(DTSTART, DTEND)
        self.assertEquals(len(events), 1)
    
    def test__A_E1_E2_B(self):
        DTSTART = self.E.DTSTART - self.E.duration()
        DTEND = self.E.DTEND + self.E.duration()
        events = Event.objects.interval(DTSTART, DTEND)
        self.assertEquals(len(events), 1)

    def test__A_E1_E2B(self):
        DTSTART = self.E.DTSTART - self.E.duration()
        DTEND = self.E.DTEND
        events = Event.objects.interval(DTSTART, DTEND)
        self.assertEquals(len(events), 1)

    def test__AE1_B_E2(self):
        DTSTART = self.E.DTSTART
        DTEND = self.E.DTSTART + self.E.duration() / 2.0
        events = Event.objects.interval(DTSTART, DTEND)
        self.assertEquals(len(events), 1)

    def test__AE1_E2B(self):
        DTSTART = self.E.DTSTART
        DTEND = self.E.DTEND
        events = Event.objects.interval(DTSTART, DTEND)
        self.assertEquals(len(events), 1)

    def test__E1_A_B_E2(self):
        DTSTART = self.E.DTSTART + self.E.duration() / 3
        DTEND = self.E.DTEND - self.E.duration() / 3
        events = Event.objects.interval(DTSTART, DTEND)
        self.assertEquals(len(events), 1)

    def test__E1_A_E2B(self):
        DTSTART = self.E.DTSTART + self.E.duration() / 2
        DTEND = self.E.DTEND
        events = Event.objects.interval(DTSTART, DTEND)
        self.assertEquals(len(events), 1)

    def test__E1_E2_A_B(self):
        DTSTART = self.E.DTEND + self.E.duration()
        DTEND = self.E.DTEND + 2 * self.E.duration()
        events = Event.objects.interval(DTSTART, DTEND)
        self.assertEquals(len(events), 0)

    def test__E1_E2A_B(self):
        DTSTART = self.E.DTEND
        DTEND = self.E.DTEND + self.E.duration()
        events = Event.objects.interval(DTSTART, DTEND)
        self.assertEquals(len(events), 0)


    # tests with DTSTART only
    def test__A_E1_E2(self):
        DTSTART = self.E.DTSTART - self.E.duration()
        events = Event.objects.interval(DTSTART=DTSTART)
        self.assertEquals(len(events), 1)

    def test__AE1_E2(self):
        DTSTART = self.E.DTSTART
        events = Event.objects.interval(DTSTART=DTSTART)
        self.assertEquals(len(events), 1)

    def test__E1_A_E2(self):
        DTSTART = self.E.DTSTART + self.E.duration() / 2 
        events = Event.objects.interval(DTSTART=DTSTART)
        self.assertEquals(len(events), 1)

    def test__E1_E2A(self):
        DTSTART = self.E.DTEND
        events = Event.objects.interval(DTSTART=DTSTART)
        self.assertEquals(len(events), 0)

    def test__E1_E2_A(self):
        DTSTART = self.E.DTEND + self.E.duration()
        events = Event.objects.interval(DTSTART=DTSTART)
        self.assertEquals(len(events), 0)


    # tests with DTEND only
    def test__B_E1_E2(self):
        DTEND = self.E.DTSTART - self.E.duration()
        events = Event.objects.interval(DTEND=DTEND)
        self.assertEquals(len(events), 0)

    def test__BE1_E2(self):
        DTEND = self.E.DTSTART
        events = Event.objects.interval(DTEND=DTEND)
        self.assertEquals(len(events), 0)

    def test__E1_B_E2(self):
        DTEND = self.E.DTSTART + self.E.duration() / 2
        events = Event.objects.interval(DTEND=DTEND)
        self.assertEquals(len(events), 1)

    def test__E1_E2B(self):
        DTEND = self.E.DTEND
        events = Event.objects.interval(DTEND=DTEND)
        self.assertEquals(len(events), 1)

    def test__E1_E2_B(self):
        DTEND = self.E.DTEND + self.E.duration()
        events = Event.objects.interval(DTEND=DTEND)
        self.assertEquals(len(events), 1)


    # test with empty interval
    def test_E1_E2(self):
        events = Event.objects.interval()
        self.assertEquals(len(events), 1)
    

    # ValueError exception tests
    def test__AB(self):
        DTSTART = datetime(2022, 1, 12, 10, 0, tzinfo=UTC)
        DTEND = DTSTART = datetime(2022, 1, 12, 10, 0, tzinfo=UTC)
        with self.assertRaises(ValueError):
            events = Event.objects.interval(DTSTART, DTEND)

    def test__B_A(self):
        DTSTART = datetime(2022, 1, 12, 10, 0, tzinfo=UTC)
        DTEND = datetime(2022, 1, 12, 9, 0, tzinfo=UTC)
        with self.assertRaises(ValueError):
            events = Event.objects.interval(DTSTART, DTEND)
