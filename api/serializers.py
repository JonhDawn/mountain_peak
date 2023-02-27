from rest_framework.serializers import ModelSerializer
from .models import Peak


class PeakSerializer(ModelSerializer):
    class Meta:
        model = Peak
        fields = Peak.get_fields()
