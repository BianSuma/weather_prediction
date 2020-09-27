from django.shortcuts import render, redirect
import pandas as pd
import warnings
import os
import sys
import traceback
import logging
import numpy as np
from weather.forms import WeatherForm
from weather.models import Weathers
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
warnings.filterwarnings('ignore')

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


def checkNanForDataFeature(y):
    y.replace('-', np.nan, inplace=True)
    y.fillna(method="ffill", inplace=True)


def checkNanForDataTarget(X):
    X.replace('-', np.nan, inplace=True)
    X.fillna(method='ffill', inplace=True)


def predict(target):
    data_cuaca = pd.read_excel('static/Weather Raw Data/Data Ta.xlsx')

    X = data_cuaca.drop(['Tanggal', 'Td_Med_C', 'Wind_Dir', 'Pres_S_Lev_Hp', 'Prec_mm', 'TotClOct', 'LowClOct', 'Sun_D_1_h', 'Vis_Km', 'Daily_Weather_Summary_09_00_00', 'Daily_Weather_Summary_12_00_00',
                         'Daily_Weather_Summary_15_00_00', 'Daily_Weather_Summary_18_00_00', 'Daily_Weather_Summary_21_00_00', 'Daily_Weather_Summary_00_00_00', 'Daily_Weather_Summary_03_00_00', 'Daily_Weather_Summary_06_00_00'], axis=1)
    y = data_cuaca['Daily_Weather_Summary_09_00_00']

    checkNanForDataFeature(y)
    checkNanForDataTarget(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y)

    tree_model = DecisionTreeClassifier(max_depth=3)

    tree_fit = tree_model.fit(X_train, y_train)

    param_dct = {
        'random_state': np.arange(21, 25),
    }

    gscv = GridSearchCV(tree_fit, param_dct,
                        scoring='accuracy', return_train_score=True)

    gscv.fit(X_train, y_train)

    return gscv.predict(target)


def index(request):
    weather = Weathers.objects.all()
    last_index = len(weather) - 1
    return render(request, 'views/home.html', {
        'weather': weather[last_index]
    })


def showWeatherDataMaster(request):
    weather_data = read_file('static/Weather Raw Data/Data Ta.xlsx')
    weathers = []
    for i in range(weather_data.shape[0]):
        temp = weather_data.iloc[i]
        weathers.append(dict(temp))

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
        target = {
            'temp_maks': data['tempmaks'],
            'temp_min': data['tempmin'],
            'temp_med': data['tempmed'],
            'hr_med': data['hrmed'],
            'wind_int': data['windint']
        }
        form = WeatherForm(request.POST)
        print(form)
        # df_target = pd.DataFrame(data=target, index=[0])
        # summary = predict(df_target)
        # print(summary)
        # form =
        return redirect('http://localhost:8000/report')
    return render(request, 'views/predict.html')
