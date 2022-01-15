from django.db import models
from django import forms
from datetime import datetime
import icalendar
from icalendar.tools import UIDGenerator
from decouple import config

UID_GENERATOR = UIDGenerator()


class Calendar(models.Model):
    name = models.CharField(max_length=24)
    
    def __str__(self):
        return self.name


class EventManager(models.Manager):
    def create(self, **kwargs):
        if kwargs.get('uid') is None:
            kwargs['uid'] = UID_GENERATOR.uid(config('DOMAIN_NAME'))

        if kwargs.get('dtend') is not None and kwargs.get('dtstart') is not None:
            if kwargs['dtend'] <= kwargs['dtstart']:
                raise ValueError('dtend cannot be less or equal to dtstart') 

        return super().create(**kwargs)

    def interval(self, dtstart=None, dtend=None):
        if dtstart is None and dtend is None:
            return self.all()

        if dtstart is None:
            qs = self.filter(dtstart__lt=dtend)
            return self.filter(dtstart__lt=dtend)

        if dtend is None:
            return self.filter(dtend__gt=dtstart)

        if dtstart >= dtend:
            raise ValueError('dtend cannot be less or equal to dtstart')

        return self.filter(dtstart__lt=dtend) & self.filter(dtend__gt=dtstart)

    @staticmethod
    def _add_from_ical_event_to_ical_event_dict(ical_event):
        ical_event_dict = {}
        fields = [field.name for field in Event._meta.get_fields()]
        for field in fields:
            ical_property = field.replace('_', '-')
            if ical_event.get(ical_property) is not None:
                if type(ical_event.get(ical_property)) is icalendar.prop.vDDDTypes:
                    ical_event_dict[field] = ical_event[ical_property].dt
                else:
                    ical_event_dict[field] = ical_event[ical_property]

        return ical_event_dict

    def create_from_ical_event(self, calendar, ical_event):
        ical_event_dict = self._add_from_ical_event_to_ical_event_dict(ical_event)

        return self.create(calendar=calendar, **ical_event_dict)


class Event(models.Model):
    calendar = models.ForeignKey(to=Calendar, on_delete=models.CASCADE)

    uid = models.TextField(primary_key=True)
    dtstart = models.DateTimeField()
    dtend = models.DateTimeField()
    summary = models.TextField()
    dtstamp = models.DateTimeField()

    description = models.TextField(null=True)
    location = models.TextField(null=True)
    contact = models.TextField(null=True)
    related_to = models.TextField(null=True)
    uri = models.URLField(null=True, max_length=2048)

    objects = EventManager()

    def duration(self):
        return self.dtend - self.dtstart

    class Meta:
        ordering = ['dtstart']

    def clean(self):
        super().clean()
        if self.dtend <= self.dtstart:
            raise forms.ValidationError('dtend cannot be less or equal to dtstart')

    def __str__(self):
        return self.summary
