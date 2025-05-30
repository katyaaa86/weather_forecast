from rest_framework import viewsets

from core.api.serializers import CitySerializer
from core.models import City


class CitySearchAPIViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
