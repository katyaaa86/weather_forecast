import pytest

from core.services.weather_api import WeatherAPIError

pytestmark = pytest.mark.django_db

def test_fetch_coordinates_success(mocker, weather_api, coordinates_response_data, city_coordinates):
    city_name = 'Moscow'
    mocker.patch(
        'core.services.weather_api.WeatherAPI._make_request',
        mocker.Mock(return_value=coordinates_response_data),
    )

    result = weather_api._fetch_coordinates(city_name)

    assert result == city_coordinates


@pytest.mark.parametrize(
    'response, error_message',
    [
        (None, 'Ошибка получения координат'),
        ({'error': True, 'reason': 'error message'}, 'error message'),
        ({'result': 'data'}, 'Ошибка получения координат'),
    ]
)
def test_fetch_coordinates_failed(mocker, weather_api, response, error_message):
    city_name = 'Moscow'
    mocker.patch(
        'core.services.weather_api.WeatherAPI._make_request',
        mocker.Mock(return_value=response),
    )

    with pytest.raises(WeatherAPIError) as e:
        weather_api._fetch_coordinates(city_name)

    assert error_message in str(e.value)


def test_fetch_current_weather(mocker, weather_api, city_coordinates, weather_response_data):
    city_name = 'Moscow'
    mocker.patch(
        'core.services.weather_api.WeatherAPI._fetch_coordinates',
        mocker.Mock(return_value=city_coordinates),
    )
    mocker.patch(
        'core.services.weather_api.openmeteo_requests.Client.weather_api',
        mocker.Mock(return_value=weather_response_data),
    )

    result = weather_api.fetch_current_weather(city_name)

    assert result == {'weather': True}

@pytest.mark.parametrize(
    'response, error_message',
    [
        (None, 'Ошибка получения прогноза'),
        ({'error': True, 'reason': 'error message'}, 'error message'),
    ]
)
def test_fetch_current_weather_failed(mocker, weather_api, city_coordinates, response, error_message):
    city_name = 'Moscow'
    mocker.patch(
        'core.services.weather_api.WeatherAPI._fetch_coordinates',
        mocker.Mock(return_value=city_coordinates),
    )
    mocker.patch(
        'core.services.weather_api.openmeteo_requests.Client.weather_api',
        mocker.Mock(return_value=response),
    )

    with pytest.raises(WeatherAPIError) as e:
        weather_api.fetch_current_weather(city_name)

    assert error_message in str(e.value)
