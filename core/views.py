from django.views import generic

from core.forms import SearchCityForm
from core.models import City, UserCity
from core.services.weather_api import WeatherAPI, WeatherAPIError


class SearchCityView(generic.FormView):
    form_class = SearchCityForm
    template_name = 'city_search.html'

    def get_or_create_city(self, city_name, user_id):
        try:
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            api = WeatherAPI()
            coordinates = api.fetch_coordinates(city_name)
            city = City(**coordinates)
            city.save()

        if user_id:
            user_city, _ = UserCity.objects.get_or_create(user_id=user_id, city=city)
            user_city.count += 1
            user_city.save()

        return city

    def _prepare_context_data(self, city_name, user_id):
        city = self.get_or_create_city(city_name, user_id)
        api = WeatherAPI()
        response = api.fetch_current_weather(city.latitude, city.longitude)
        df = api.generate_dataframe(response)
        return df

    def form_valid(self, form):
        city_name = form.cleaned_data['city_name'].capitalize()
        context = self.get_context_data(form=form)
        try:
            df = self._prepare_context_data(city_name, self.request.user.id)
            context['weather_data'] = df.to_dict(orient='records')
        except WeatherAPIError as e:
            context['error'] = str(e)
        return self.render_to_response(context)
