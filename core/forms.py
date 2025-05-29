from django import forms


class SearchCityForm(forms.Form):
    city_name = forms.CharField(label='Введите город', max_length=100)