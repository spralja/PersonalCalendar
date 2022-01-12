from django.db import models
from django import forms


class EventManager(models.Manager):
    def interval(self, start_time, end_time):
        if start_time >= end_time:
            raise ValueError("start_time must be smaller than end_time")
        return self.filter(start_time__lt=end_time) & self.filter(end_time__gt=start_time)


class Event(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name = models.CharField(max_length=200)

    objects = EventManager()

    def duration(self):
        return self.end_time - self.start_time

    class Meta:
        ordering = ['start_time']
    def clean(self):
        super().clean()
        if self.end_time <= self.start_time:
            raise forms.ValidationError("End time must be after start time!")

    def __str__(self):
        return self.name
