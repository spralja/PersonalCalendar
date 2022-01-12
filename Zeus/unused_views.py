from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer 
from datetime import datetime

class EventIntervalAPIView(APIView):

    def get(self, request, start_time_isoformat, end_time_isoformat):
        try:
            start_time = datetime.fromisoformat(start_time_isoformat)
            end_time = datetime.fromisoformat(end_time_isoformat)        
        except ValueError as e:
            return Response({'ValueError': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if(end_time < start_time):
            return Response({'ValueError': 'End time must not be less than start time'})
        events = Event.objects.filter(start_time__lte=end_time) | Event.objects.filter(end_time__gte=start_time)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self):
        pass