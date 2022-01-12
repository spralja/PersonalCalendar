from django.urls import path
from django.http import HttpResponse

from . import views

urlpatterns = [
    path('events/interval/<str:start_time_isoformat>/<str:end_time_isoformat>/', views.EventList.as_view())
]