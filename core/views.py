from typing import Optional
from urllib import parse

from django.views import generic
from pandas import DataFrame

from core.forms import SearchCityForm
from core.models import City, UserCity
from core.services.weather_api import WeatherAPI, WeatherAPIError


class SearchCityView(generic.FormView):
    form_class = SearchCityForm
    template_name = 'city_search.html'

    def _get_or_create_city(self, city_name: str, user_id: Optional[int]) -> City:
        try:
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            api = WeatherAPI()
            coordinates = api.fetch_coordinates(city_name)
            city = City(**coordinates)
            city.save()

        user_city, _ = UserCity.objects.get_or_create(user_id=user_id, city=city)
        user_city.count += 1
        user_city.save()

        return city

    def _prepare_context_data(self, city_name: str, user_id: Optional[int]) -> DataFrame:
        city = self._get_or_create_city(city_name, user_id)
        api = WeatherAPI()
        response = api.fetch_current_weather(city.latitude, city.longitude)
        df = api.generate_dataframe(response)
        return df

    def get(self, request, *args, **kwargs):
        last_city = request.COOKIES.get('last_city')
        form = self.get_form()
        context = self.get_context_data(form=form)
        if last_city:
            context['last_city'] = parse.unquote(last_city)
        return self.render_to_response(context)

    def get_initial(self):
        initial = super().get_initial()
        last_city = self.request.COOKIES.get('last_city')
        if last_city:
            initial['city_name'] = parse.unquote(last_city)
        return initial

    def form_valid(self, form):
        city_name = form.cleaned_data['city_name'].title()
        context = self.get_context_data(form=form)
        try:
            df = self._prepare_context_data(city_name, self.request.user.id)
            context['weather_data'] = df.to_dict(orient='records')
        except WeatherAPIError as e:
            context['error'] = str(e)
        response = self.render_to_response(context)
        response.set_cookie('last_city', parse.quote(city_name))
        return response
