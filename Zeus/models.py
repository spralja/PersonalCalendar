from django.db import models
from django import forms

class Event(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name = models.CharField(max_length=200)
    class Meta:
        ordering = ['start_time']
    def clean(self):
        super().clean()
        if self.end_time <= self.start_time:
            raise forms.ValidationError("End time must be after start time!")

    def __str__(self):
        return self.name
