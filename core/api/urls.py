from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api import views

router = DefaultRouter()
router.register('city_search', views.CitySearchAPIViewSet, basename='city')
urlpatterns = [
    path('', include(router.urls)),
]