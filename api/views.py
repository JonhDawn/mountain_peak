from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import PeakSerializer
from .models import Peak


class PeakAPIView(APIView):

    def get_fields(self):
        name = self.request.POST.get('name')
        lat = float(self.request.POST.get('lat'))
        lon = (float(self.request.POST.get('lon')) + 180) % 360 - 180  # between -180° and 180° (360° = 0°)
        altitude = float(self.request.POST.get('altitude'))
        return name, lat, lon, altitude

    def get(self, *args, **kwargs):
        name = self.request.GET.get('name')
        try:
            peaks = Peak.objects.get(name=name)
        except Peak.DoesNotExist:
            return Response(data={'error': 'No such peak'}, status=500)
        else:
            serializer = PeakSerializer(peaks)
            return Response(serializer.data)

    def post(self, *args, **kwargs):
        name, lat, lon, altitude = self.get_fields()
        try:
            peaks = Peak.objects.create(lat=lat, lon=lon, altitude=altitude, name=name)
        except ValidationError:
            return Response(data={'error': 'this name already exists or the peak is too high'}, status=500)
        else:
            serializer = PeakSerializer(peaks)
            return Response(serializer.data)

    def delete(self, *args, **kwargs):
        name = self.request.POST.get('name')
        peaks = Peak.objects.filter(name=name)
        if peaks.exists():
            peaks.delete()
            return Response(data={'action': f'{name} has been deleted'})
        else:
            return Response(data={'error': 'this peak does not exist'}, status=500)

    def put(self, *args, **kwargs):
        name, lat, lon, altitude = self.get_fields()
        peaks = Peak.objects.filter(name=name)
        if peaks.exists():
            peak = peaks[0]
            if lat is not None:
                peak.lat = lat
            if lon is not None:
                peak.lon = lon
            if altitude is not None:
                peak.altitude = altitude
            try:
                peak.full_clean()
            except ValidationError:
                return Response(data={'error': 'the peak is too high'}, status=500)
            else:
                peak.save()
                serializer = PeakSerializer(peak)
                return Response(serializer.data)
        else:
            return Response(data={'error': 'this peak does not exist'}, status=500)


class ZoneAPIView(APIView):

    def get(self, *args, **kwargs):
        lat_ne = float(self.request.GET.get('lat_ne'))
        lat_sw = float(self.request.GET.get('lat_sw'))
        lon_ne = float(self.request.GET.get('lon_ne'))
        lon_sw = float(self.request.GET.get('lon_sw'))
        if lon_ne < lon_sw:
            peaks = Peak.objects.filter(~Q(lon__range=(lon_ne, lon_sw)), lat__range=(lat_sw, lat_ne))
        else:
            peaks = Peak.objects.filter(lon__range=(lon_sw, lon_ne), lat__range=(lat_sw, lat_ne))
        serializer = PeakSerializer(peaks, many=True)
        return Response(serializer.data)
