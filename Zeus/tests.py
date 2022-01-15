from django.test import TestCase
from .models import Calendar, Event, EventManager
from datetime import datetime, timezone, timedelta
import icalendar


UTC = timezone.utc
DTSTAMP = datetime.now(tz=UTC)


class EventTestCase(TestCase):
    def setUp(self):
        self.CAL = Calendar.objects.create(name='dummy')

    def test_duration(self):
        event = Event(
            dtstart=datetime(2022, 1, 12, 9, 0, tzinfo=UTC),
            dtend=datetime(2022, 1, 12, 10, 0, tzinfo=UTC),
            summary='Breakfast',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        self.assertEquals(event.duration(), timedelta(hours=1))

    
    # ordering tests

    # E1 = E.dtstart
    # E2 = E.dtend
    # F1 = F.dtstart
    # F2 = F.dtend

    def test__E1_E2_F1_f2(self):
        E = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            dtend=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            summary='Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        F = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 22, 0, tzinfo=UTC),
            dtend = datetime(2022, 1, 13, 23, 0, tzinfo=UTC),
            summary='Second Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1_E2F1_F2(self):
        E = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            dtend=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            summary='Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        F = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            dtend = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            summary='Second Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1_F1_E2_F2(self):
        E = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            dtend=datetime(2022, 1, 12, 22, 0, tzinfo=UTC),
            summary='Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        F = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            dtend = datetime(2022, 1, 13, 23, 0, tzinfo=UTC),
            summary='Second Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1_F1_E2F2(self):
        E = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            dtend=datetime(2022, 1, 12, 22, 0, tzinfo=UTC),
            summary='Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        F = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            dtend = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            summary='Second Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], E)
        self.assertEquals(events[1], F)

        events.delete()

    def test__E1F1_E2_F2(self):
        E = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            dtend=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            summary='Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        F = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            dtend = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            summary='Second Dinner',
            dtstamp=DTSTAMP,
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
            dtstart=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            dtend=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            summary='Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        F = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 19, 0, tzinfo=UTC),
            dtend = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            summary='Second Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], F)
        self.assertEquals(events[1], E)

        events.delete()

    def test__F1_E1_E2F2(self):
        E = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            dtend=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            summary='Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        F = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 19, 0, tzinfo=UTC),
            dtend = datetime(2022, 1, 13, 21, 0, tzinfo=UTC),
            summary='Second Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        events = Event.objects.all()
        self.assertEquals(events[0], F)
        self.assertEquals(events[1], E)

        events.delete()

    def test__F1E1_E2_F2(self):
        E = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            dtend=datetime(2022, 1, 12, 21, 0, tzinfo=UTC),
            summary='Dinner',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

        F = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 20, 0, tzinfo=UTC),
            dtend = datetime(2022, 1, 13, 22, 0, tzinfo=UTC),
            summary='Second Dinner',
            dtstamp=DTSTAMP,
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
        dtstart = datetime(2022, 1, 15, 16, 6, tzinfo=UTC)
        dtend = datetime(2022, 1, 15, 16, 5, tzinfo=UTC)
        with self.assertRaises(ValueError):
            Event.objects.create(
                dtstart=dtstart,
                dtend=dtend,
                summary='dummy',
                dtstamp=DTSTAMP,
                calendar=self.CAL,
            )

            Event.objects.delete()

    def test_create_raises_validation_error_T1T2(self):
        dtstart = datetime(2022, 1, 15, 16, 6, tzinfo=UTC)
        dtend = datetime(2022, 1, 15, 16, 6, tzinfo=UTC)
        with self.assertRaises(ValueError):
            Event.objects.create(
                dtstart=dtstart,
                dtend=dtend,
                summary='dummy',
                dtstamp=DTSTAMP,
                cal=self.CAL,
            )

            Event.objects.delete()

    def test_create_from_ical_event(self):
        ical_file = open('test/cal.ics', 'rb')
        ical_cal = icalendar.Calendar.from_ical(ical_file.read())
        ical_file.close()

        ical_event = ical_cal.subcomponents[1]
        
        E = Event.objects.create_from_ical_event(self.CAL, ical_event)
        self.assertEquals(E.related_to, 'test')


class EventManagerIntervalTestCase(TestCase):
    def setUp(self):
        self.CAL = Calendar.objects.create(name='dummy')

        self.E = Event.objects.create(
            dtstart=datetime(2022, 1, 12, 10, 0, tzinfo=UTC),
            dtend=datetime(2022, 1, 12, 11, 0, tzinfo=UTC),
            summary='Second Breakfast',
            dtstamp=DTSTAMP,
            calendar=self.CAL,
        )

    # A = dtstart
    # B = dtend
    # E1 = E.dtstart
    # E2 = E.dtend


    # tests with dtstart and dtendd
    def test__A_B_E1_E2(self):
        dtstart = self.E.dtstart - 2 * self.E.duration()
        dtend = self.E.dtstart - self.E.duration()
        events = Event.objects.interval(dtstart, dtend)
        self.assertEquals(len(events), 0)

    def test__A_BE1_E2(self):
        dtstart = self.E.dtstart - self.E.duration()
        dtend = self.E.dtstart
        events = Event.objects.interval(dtstart, dtend)
        self.assertEquals(len(events), 0)

    def test__A_E1_B_E2(self):
        dtstart = self.E.dtstart - self.E.duration()
        dtend = self.E.dtstart + self.E.duration() / 2.0
        events = Event.objects.interval(dtstart, dtend)
        self.assertEquals(len(events), 1)
    
    def test__A_E1_E2_B(self):
        dtstart = self.E.dtstart - self.E.duration()
        dtend = self.E.dtend + self.E.duration()
        events = Event.objects.interval(dtstart, dtend)
        self.assertEquals(len(events), 1)

    def test__A_E1_E2B(self):
        dtstart = self.E.dtstart - self.E.duration()
        dtend = self.E.dtend
        events = Event.objects.interval(dtstart, dtend)
        self.assertEquals(len(events), 1)

    def test__AE1_B_E2(self):
        dtstart = self.E.dtstart
        dtend = self.E.dtstart + self.E.duration() / 2.0
        events = Event.objects.interval(dtstart, dtend)
        self.assertEquals(len(events), 1)

    def test__AE1_E2B(self):
        dtstart = self.E.dtstart
        dtend = self.E.dtend
        events = Event.objects.interval(dtstart, dtend)
        self.assertEquals(len(events), 1)

    def test__E1_A_B_E2(self):
        dtstart = self.E.dtstart + self.E.duration() / 3
        dtend = self.E.dtend - self.E.duration() / 3
        events = Event.objects.interval(dtstart, dtend)
        self.assertEquals(len(events), 1)

    def test__E1_A_E2B(self):
        dtstart = self.E.dtstart + self.E.duration() / 2
        dtend = self.E.dtend
        events = Event.objects.interval(dtstart, dtend)
        self.assertEquals(len(events), 1)

    def test__E1_E2_A_B(self):
        dtstart = self.E.dtend + self.E.duration()
        dtend = self.E.dtend + 2 * self.E.duration()
        events = Event.objects.interval(dtstart, dtend)
        self.assertEquals(len(events), 0)

    def test__E1_E2A_B(self):
        dtstart = self.E.dtend
        dtend = self.E.dtend + self.E.duration()
        events = Event.objects.interval(dtstart, dtend)
        self.assertEquals(len(events), 0)


    # tests with dtstart only
    def test__A_E1_E2(self):
        dtstart = self.E.dtstart - self.E.duration()
        events = Event.objects.interval(dtstart=dtstart)
        self.assertEquals(len(events), 1)

    def test__AE1_E2(self):
        dtstart = self.E.dtstart
        events = Event.objects.interval(dtstart=dtstart)
        self.assertEquals(len(events), 1)

    def test__E1_A_E2(self):
        dtstart = self.E.dtstart + self.E.duration() / 2 
        events = Event.objects.interval(dtstart=dtstart)
        self.assertEquals(len(events), 1)

    def test__E1_E2A(self):
        dtstart = self.E.dtend
        events = Event.objects.interval(dtstart=dtstart)
        self.assertEquals(len(events), 0)

    def test__E1_E2_A(self):
        dtstart = self.E.dtend + self.E.duration()
        events = Event.objects.interval(dtstart=dtstart)
        self.assertEquals(len(events), 0)


    # tests with dtend only
    def test__B_E1_E2(self):
        dtend = self.E.dtstart - self.E.duration()
        events = Event.objects.interval(dtend=dtend)
        self.assertEquals(len(events), 0)

    def test__BE1_E2(self):
        dtend = self.E.dtstart
        events = Event.objects.interval(dtend=dtend)
        self.assertEquals(len(events), 0)

    def test__E1_B_E2(self):
        dtend = self.E.dtstart + self.E.duration() / 2
        events = Event.objects.interval(dtend=dtend)
        self.assertEquals(len(events), 1)

    def test__E1_E2B(self):
        dtend = self.E.dtend
        events = Event.objects.interval(dtend=dtend)
        self.assertEquals(len(events), 1)

    def test__E1_E2_B(self):
        dtend = self.E.dtend + self.E.duration()
        events = Event.objects.interval(dtend=dtend)
        self.assertEquals(len(events), 1)


    # test with empty interval
    def test_E1_E2(self):
        events = Event.objects.interval()
        self.assertEquals(len(events), 1)
    

    # ValueError exception tests
    def test__AB(self):
        dtstart = datetime(2022, 1, 12, 10, 0, tzinfo=UTC)
        dtend = dtstart = datetime(2022, 1, 12, 10, 0, tzinfo=UTC)
        with self.assertRaises(ValueError):
            events = Event.objects.interval(dtstart, dtend)

    def test__B_A(self):
        dtstart = datetime(2022, 1, 12, 10, 0, tzinfo=UTC)
        dtend = datetime(2022, 1, 12, 9, 0, tzinfo=UTC)
        with self.assertRaises(ValueError):
            events = Event.objects.interval(dtstart, dtend)
