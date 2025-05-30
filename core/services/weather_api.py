import openmeteo_requests
import pandas as pd
import requests
import requests_cache
from retry_requests import retry

class WeatherAPIError(Exception):
    pass


class WeatherAPI:
    def __init__(self):
        self.geo_url = 'https://geocoding-api.open-meteo.com/v1/search'
        self.weather_url = 'https://api.open-meteo.com/v1/forecast'

        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)

    def fetch_coordinates(self, city_name):
        params = {'name': city_name, 'count': 1, 'language': 'ru'}

        response = self._make_request(self.geo_url, params=params)
        if not response:
            raise WeatherAPIError('Ошибка получения координат')
        if 'error' in response:
            raise WeatherAPIError(response.get('reason'))

        results = response.get('results')
        if not results:
            raise WeatherAPIError('Ошибка получения координат')
        city_info = results[0]
        return {
            'latitude': city_info['latitude'],
            'longitude': city_info['longitude'],
            'name':city_info['name'],
            'country': city_info['country'],
        }

    def fetch_current_weather(self, latitude, longitude):
        params = {'latitude': latitude, 'longitude': longitude, 'hourly': 'temperature_2m'}
        try:
            response = self.openmeteo.weather_api(self.weather_url, params=params)
        except Exception as e:
            raise WeatherAPIError(str(e))

        if not response:
            raise WeatherAPIError('Ошибка получения прогноза')
        if 'error' in response:
            raise WeatherAPIError(response.get('reason'))

        return response[0]

    def _make_request(self, url, method='GET', params=None, data=None):
        try:
            response = requests.request(method, url, params=params, data=data)
            response_data = response.json()
        except Exception as e:
            raise WeatherAPIError(str(e))

        return response_data

    def generate_dataframe(self, response):
        hourly = response.Hourly()

        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "temperature_2m": hourly_temperature_2m.round().astype(int),
        }

        df = pd.DataFrame(data=hourly_data)
        return df

