import pytest

from core.services.weather_api import WeatherAPI


@pytest.fixture
def weather_api():
    return WeatherAPI()

@pytest.fixture
def coordinates_response_data():
    return {"results": [
        {
            "id": 2950159,
            "name": "Berlin",
            "latitude": 52.52437,
            "longitude": 13.41053,
            "elevation": 74.0,
            "feature_code": "PPLC",
            "country_code": "DE",
            "admin1_id": 2950157,
            "admin2_id": 0,
            "admin3_id": 6547383,
            "admin4_id": 6547539,
            "timezone": "Europe/Berlin",
            "population": 3426354,
            "postcodes": [
                "10967",
                "13347"
            ],
            "country_id": 2921044,
            "country": "Deutschland",
            "admin1": "Berlin",
            "admin2": "",
            "admin3": "Berlin, Stadt",
            "admin4": "Berlin"
        }]}

@pytest.fixture
def city_coordinates():
    return {'latitude': 52.52437, 'longitude': 13.41053, "name": "Berlin", "country": "Deutschland"}

@pytest.fixture
def weather_response_data():
    return [{'weather': True}]