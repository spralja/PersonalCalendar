from django.db import models
from django import forms
from datetime import datetime
import icalendar
from icalendar.tools import UIDGenerator
from decouple import config


class generate_uid:
    UID_GENERATOR = UIDGenerator()

    @staticmethod
    def __call__():
        return generate_uid.UID_GENERATOR.uid(config('DOMAIN_NAME'))


class ICalendarElementManager(models.Manager):
    def create_from_ical_element(self, ical_element, **kwargs):
        element_dict = self._convert_properties(ical_element)
        element_dict.update(kwargs)

        return self.create(**element_dict)


    def _convert_properties(self, ical_element):
        element_dict = {}
        fields = [field.name for field in self.model._meta.get_fields()]
        for field in fields:
            ical_property = field.replace('_', '-')
            if ical_element.get(ical_property) is not None:
                if type(ical_element[ical_property]) is icalendar.prop.vDDDTypes:
                    element_dict[field] = ical_element[ical_property].dt
                else:
                    element_dict[field] = ical_element[ical_property]

        return element_dict

class Calendar(models.Model):
    name = models.CharField(max_length=24)
    
    def __str__(self):
        return self.name


class EventManager(ICalendarElementManager):
    def create(self, **kwargs):
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


class Event(models.Model):
    calendar = models.ForeignKey(to=Calendar, on_delete=models.CASCADE)

    uid = models.TextField(default=generate_uid.__call__, primary_key=True)
    dtstart = models.DateTimeField()
    dtend = models.DateTimeField()
    summary = models.TextField()
    dtstamp = models.DateTimeField()

    description = models.TextField(null=True)
    location = models.TextField(null=True)
    contact = models.TextField(null=True)
    related_to = models.TextField(null=True)
    uri = models.URLField(null=True, max_length=2048)
    last_modified = models.DateTimeField(null=True)
    created = models.DateTimeField(null=True)
    sequence = models.IntegerField(null=True)

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
