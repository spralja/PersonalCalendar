from django.db import models
from django import forms
from datetime import datetime
import icalendar


class Calendar(models.Model):
    name = models.CharField(max_length=24)
    
    def __str__(self):
        return self.name


class EventManager(models.Manager):
    def create(self, **kwargs):
        if kwargs.get('DTEND') is not None and kwargs.get('DTSTART') is not None:
            if kwargs['DTEND'] <= kwargs['DTSTART']:
                raise ValueError('DTEND cannot be less or equal to DTSTART') 
        
        return super().create(**kwargs)

    def interval(self, DTSTART=None, DTEND=None):
        if DTSTART is None and DTEND is None:
            return self.all()

        if DTSTART is None:
            qs = self.filter(DTSTART__lt=DTEND)
            return self.filter(DTSTART__lt=DTEND)

        if DTEND is None:
            return self.filter(DTEND__gt=DTSTART)

        if DTSTART >= DTEND:
            raise ValueError('DTEND cannot be less or equal to DTSTART')

        return self.filter(DTSTART__lt=DTEND) & self.filter(DTEND__gt=DTSTART)

    def _add_from_ical_event_to_ical_event_dict(ical_event, ical_event_dict, *args):
        for arg in args:
            if ical_event.get(arg) is not None:
                ical_event_dict[arg] = ical_event[arg].t


    def create_from_ical_event(self, ical_event, calendar):
        ical_event_dict = {}
        if ical_event.get('DTSTART') is not None:
            ical_event_dict['DTSTART'] = ical_event['DTSTART'].dt

        if ical_event.get('DTEND') is not None:
            ical_event_dict['DTEND'] = ical_event['DTEND'].dt

        _add_from_ical_event_to_ical_event_dict(ical_event, ical_event_dict,
            'UID', 'SUMMARY', 'DESCRIPTION', 'LOCATION', 'DTSSTAMP',
        )

        return self.create(calendar=calendar, **ical_event_dict)


class Event(models.Model):
    calendar = models.ForeignKey(to=Calendar, on_delete=models.CASCADE)

    UID = models.TextField(primary_key=True)
    DTSTART = models.DateTimeField()
    DTEND = models.DateTimeField()
    SUMMARY = models.CharField(max_length=200)
    DESCRIPTION = models.TextField(blank=True)
    LOCATION = models.TextField(blank=True)
    DTSSTAMP = models.DateTimeField()

    objects = EventManager()

    def duration(self):
        return self.DTEND - self.DTSTART

    class Meta:
        ordering = ['DTSTART']

    def clean(self):
        super().clean()
        if self.DTEND <= self.DTSTART:
            raise forms.ValidationError('DTEND cannot be less or equal to DTSTART')

    def __str__(self):
        return self.SUMMARY
