from django.db.models import Sum
from rest_framework import serializers

from core.models import City


class CitySerializer(serializers.ModelSerializer):
    search_count = serializers.SerializerMethodField(method_name='count_city_search')

    class Meta:
        model = City
        fields = ['id', 'url', 'name', 'latitude', 'longitude', 'search_count']

    def count_city_search(self, obj):
        return obj.users.aggregate(total=Sum('count')).get('total') or 0