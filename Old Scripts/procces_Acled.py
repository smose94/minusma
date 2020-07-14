#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 16:44:54 2020

@author: simon
"""
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc


data = pd.read_csv('Processed_Acled_Mali.csv')

years_active = ['2013','2014','2015','2016','2017','2018','2019','2020']
map_data = data.drop('Unnamed: 0',axis=1)
map_data = map_data[map_data['year'].isin(years_active)]
map_data['year'] = map_data['year'].astype('category')
map_data['event_date'] = pd.to_datetime(map_data['event_date'])

#Set up datetime object to get today's date
today = pd.Timestamp(dt.date.today())
start_delta = dt.timedelta(weeks=2)
last_week = pd.Timestamp(today - start_delta)
mask = (map_data['event_date'] > last_week) & (map_data['event_date'] <= today)
week_fatalities = int(map_data.loc[mask]['fatalities'].sum())
total_fatalities = int(map_data['fatalities'].sum())

