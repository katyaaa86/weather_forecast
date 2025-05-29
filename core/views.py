from django.views import generic

from core.forms import SearchCityForm
from core.services.weather_api import WeatherAPI, WeatherAPIError


class SearchCityView(generic.FormView):
    form_class = SearchCityForm
    template_name = 'city_search.html'

    def _prepare_context_data(self, city_name):
        api = WeatherAPI()
        response = api.fetch_current_weather(city_name)
        df = api.generate_dataframe(response)
        return df

    def form_valid(self, form):
        city_name = form.cleaned_data['city_name']
        context = self.get_context_data(form=form)

        try:
            df = self._prepare_context_data(city_name)
            context['weather_data'] = df.to_dict(orient='records')
        except WeatherAPIError as e:
            context['error'] = str(e)
        return self.render_to_response(context)
