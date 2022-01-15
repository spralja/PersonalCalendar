from django.db import models
from django import forms
from datetime import datetime
import icalendar


class Calendar(models.Model):
    name = models.CharField(max_length=24)
    
    def __str__(self):
        return self.name


class EventManager(models.Manager):
    def create(self, *args, **kwargs):
        if kwargs.get('DTEND') <= kwargs.get('DTSTART'):
            raise ValueError('DTEND cannot be less or equal to DTSTART') 
        
        return super().create(*args, **kwargs)

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

    def create_from_ical_event(self, ical_event, calendar):
        ical_event_dict = {}
        if ical_event.get('DTSTART') is not None:
            ical_event_dict['DTSTART'] = ical_event['DTSTART'].dt

        if ical_event.get('DTEND') is not None:
            ical_event_dict['DTEND'] = ical_event['DTEND'].dt

        if ical_event.get('SUMMARY') is not None:
            ical_event_dict['SUMMARY'] = ical_event['SUMMARY']

        return self.create(calendar=calendar, **ical_event_dict)


class Event(models.Model):
    calendar = models.ForeignKey(to=Calendar, on_delete=models.CASCADE)

    DTSTART = models.DateTimeField()
    DTEND = models.DateTimeField()
    SUMMARY = models.CharField(max_length=200)

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
        return self.name
