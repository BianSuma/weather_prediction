from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('report', views.showReport, name='report'),
    path('master', views.showWeatherDataMaster, name='data_master'),
    path('predict', views.showPredictPage, name='predict'),
]
