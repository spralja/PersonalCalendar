from django.db import models
from django import forms
from datetime import datetime
import icalendar
from icalendar.tools import UIDGenerator
from decouple import config
from enum import Enum

class Conformance(Enum):
    CAN_BE_SPECIFIED = 0
    MUST_BE_SPECIFIED = 1
    CAN_BE_SPECIFIED_MULTIPLE_TIMES = 2

class PropertyClass:
    _value_data_type_switch = {
        'BINARY': NotImplementedError(),
        'BOOLEAN': models.BooleanField,
        'CAL-ADDRESS': NotImplementedError(),
        'DATE': NotImplementedError(),
        'DATE-TIME': models.DateTimeField,
        'DURATION': NotImplementedError(),
        'FLOAT': models.FloatField,
        'INTEGER': models.IntegerField,
        'PERIOD': NotImplementedError(),
        'RECUR': NotImplementedError(),
        'TEXT': models.TextField,
        'TIME': NotImplementedError(),
        'URI': NotImplementedError(),
        'UTC-OFFSET': NotImplementedError()
    }

    def __call__(self, value_data_type, conformance, shared=False, **options):
        if type(value_data_type) is not str:
            raise TypeError('value_data_type must be str')

        value_data_type = value_data_type.upper()
        field = None
        if self._value_data_type_switch.get(value_data_type) is not None:
            if type(self._value_data_type_switch[value_data_type]) is NotImplementedError:
                raise self._value_data_type_switch[value_data_type]

            field = self._value_data_type_switch[value_data_type]   
        else:
            raise TypeError('valu_data_type is not registerd')

        if type(conformance) is not Conformance:
            raise TypeError('conformance must be of type Conformance')

        if conformance == Conformance.CAN_BE_SPECIFIED:
            if options.get('primary_key') is not None:
                if options['primary_key'] != False:
                    raise TypeError('if conformance is CAN_BE_SPECIFIED, primary_key must not not be False')
            
            if options.get('null') is not None:
                if options['null'] != True:
                    raise TypeError()

            options['null'] = True
        elif conformance == Conformance.MUST_BE_SPECIFIED:
            if options.get('null') is not None:
                if options['null'] != False:
                    raise TypeError()
            
            options['null'] = False
        else:
            if field is not None:
                raise TypeError()
            else:
                if options.get('to') is not None:
                    raise TypeError()

                if options.get('on_delete') is None:
                    raise TypeError()

                raise NotImplementedError()

            raise NotImplementedError()

        if shared:
            raise NotImplementedError()


        return field(**options)

PropertyField = PropertyClass()

class GenerateUIDClass:
    UID_GENERATOR = UIDGenerator()

    @staticmethod
    def __call__():
        return generate_uid.UID_GENERATOR.uid(config('DOMAIN_NAME'))

generate_uid = GenerateUIDClass()

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
            if ical_property[0] == '-':
                ical_property = ical_property[1:]

            if ical_element.get(ical_property) is not None:
                if type(ical_element[ical_property]) is icalendar.prop.vDDDTypes:
                    element_dict[field] = ical_element[ical_property].dt
                elif type(ical_element[ical_property]) is icalendar.prop.vGeo:
                    geo_dict = vars(ical_element[ical_property])
                    geo_dict.pop('params')
                    element_dict[field] = Geo.objects.create(**geo_dict)
                else:
                    element_dict[field] = ical_element[ical_property]

        return element_dict


class CalendarManager(ICalendarElementManager):
    def create_from_ical(self, ical, **kwargs):
        ical_cal = icalendar.Calendar.from_ical(ical)
        calendar = self.create_from_ical_element(ical_cal, ical=ical, **kwargs)

        for subcomponent in ical_cal.subcomponents:
            if type(subcomponent) is icalendar.cal.Event:
                Event.objects.create_from_ical_element(subcomponent, calendar=calendar)

        return calendar


class Calendar(models.Model):
    name = models.TextField(blank=False, null=False)
    ical = models.TextField()

    prodid = models.TextField(primary_key=True, default=generate_uid.__call__)

    objects = CalendarManager()
    
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
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, null=True)

    uid = PropertyField('TEXT', Conformance.MUST_BE_SPECIFIED, default=generate_uid.__call__, primary_key=True)
    dtstart = PropertyField('DATE-TIME', Conformance.MUST_BE_SPECIFIED)
    dtend = PropertyField('DATE-TIME', Conformance.MUST_BE_SPECIFIED)
    summary = PropertyField('TEXT', Conformance.CAN_BE_SPECIFIED)
    dtstamp = PropertyField('DATE-TIME', Conformance.MUST_BE_SPECIFIED )

    objects = EventManager()

    def duration(self):
        return self.dtend - self.dtstart

    class Meta:
        ordering = ['dtstart']

    def __str__(self):
        return self.summary
