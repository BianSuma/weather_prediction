from django.shortcuts import render, redirect
import pandas as pd
import os
import sys
import traceback
import logging
from weather.forms import WeatherForm
from weather.models import Weathers

# Create your views here.


def read_file(filename, **kwargs):
    """ Read file with **kwargs; files supported: xls, xlsx, csv, csv.gz, pkl """

    read_map = {
        'xls': pd.read_excel,
        'xlsx': pd.read_excel,
        'csv': pd.read_csv,
        'gz': pd.read_csv,
        'pkl': pd.read_pickle
    }

    ext = os.path.splitext(filename)[1].lower()[1:]
    assert ext in read_map, "Input file not correct in format, must be xls, xlsx, csv, gz, pkl; current format '{0}'".format(
        ext)
    assert os.path.isfile(filename), "File not found '{0}'.".format(filename)

    return read_map[ext](filename, **kwargs)


def predict(mdl):
    print('Model')


def index(request):
    weather = Weathers.objects.all()
    return render(request, 'views/home.html', {
        'weather': weather[0]
    })


def showWeatherDataMaster(request):
    weather_data = read_file('static/Weather Raw Data/Data Ta.xlsx')
    weathers = {
        'tanggal': weather_data['Tanggal'],
        'temp_maks': weather_data['Temperature Max'],
        'temp_min': weather_data['Temperature Min'],
        'temp_med': weather_data['Temperature Med'],
        'td_med': weather_data['Td. Med (C)'],
        'hr_med': weather_data['Hr. Med (%)'],
        'wind_dir': weather_data['Wind (km/h) Dir.'],
        'wind_int': weather_data['Wind (km/h) Int.'],
        'pres_lev': weather_data['Pres. S. Lev (Hp)'],
        'prec': weather_data['Prec. (mm)'],
        'totcloct': weather_data['TotClOct'],
        'lowcloct': weather_data['LowClOct'],
        'sun': weather_data['Sun D-1 (h)'],
        'vis_km': weather_data['Vis Km'],
        'sum_09': weather_data['Daily Weather Summary 09.00.00'],
        'sum_12': weather_data['Daily Weather Summary 12.00.00'],
        'sum_15': weather_data['Daily Weather Summary 15.00.00'],
        'sum_18': weather_data['Daily Weather Summary 18.00.00'],
        'sum_21': weather_data['Daily Weather Summary 21.00.00'],
        'sum_00': weather_data['Daily Weather Summary 00.00.00'],
        'sum_03': weather_data['Daily Weather Summary 03.00.00'],
        'sum_06': weather_data['Daily Weather Summary 06.00.00'],
    }

    return render(request, 'views/master.html', {
        'weathers': weathers
    })


def showReport(request):
    weathers = Weathers.objects.all()
    return render(request, 'views/report.html', {
        'weathers': weathers
    })


def showPredictPage(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        print(sys.stderr)
        try:
            weather = Weathers.objects.create()
            print('Submit has been clicked')
            return redirect('http://localhost:8000/report')
        except:
            print(sys.stderr)
    return render(request, 'views/predict.html')
