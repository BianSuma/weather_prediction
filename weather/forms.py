from django import forms
from weather.models import Weathers


class WeatherForm(forms.ModelForm):
    class Meta:
        model = Weathers
        fields = "__all__"
