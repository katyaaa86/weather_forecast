from django.urls import path

from core.views import SearchCityView

urlpatterns = [
    path('', SearchCityView.as_view(), name='search_city'),
]