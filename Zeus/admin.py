from django.contrib import admin

from .models import Event, Calendar, Geo

admin.site.register(Event)
admin.site.register(Calendar)
admin.site.register(Geo)