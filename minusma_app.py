#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 12:21:27 2020

@author: simon
"""


import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import datetime as dt
from pytz import timezone
gmt = timezone('GMT')

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc


colors = {
    'background': 'rgb(240,240,230)',
    'text': 'rgb(0, 118, 192)'
}

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div([
    
    dcc.Interval(
            id='my_interval',
            disabled=False,     #if True, the counter will no longer update
            interval=1*30000,#increment the counter n_intervals every interval milliseconds
            n_intervals=0,      #number of times the interval has passed
            max_intervals=-1,    #number of times the interval will be fired.
                                #if -1, then the interval has no limit (the default)
                                #and if 0 then the interval stops running.
                                ),
    dcc.Interval(
            id='my_interval_graphs',
            disabled=False,     #if True, the counter will no longer update
            interval=1*1800000,#increment the counter n_intervals every interval milliseconds
            n_intervals=0,      #number of times the interval has passed
            max_intervals=-1,    #number of times the interval will be fired.
                                #if -1, then the interval has no limit (the default)
                                #and if 0 then the interval stops running.
                                ),
    
    dbc.Row(children = [
        dbc.NavbarSimple(
            children=[  
            dbc.NavItem(dbc.NavLink("United Nations Peacekeeping", href="https://peacekeeping.un.org/en'")),
            dbc.NavItem(dbc.NavLink("Project Github", href="https://github.com/smose94/minusma")),
            dbc.NavItem(dbc.NavLink("ACLED", href="https://acleddata.com")),
            dbc.NavItem(dbc.NavLink("MINUSMA Home", href="https://minusma.unmissions.org/en"))
            
            
        ], 
            brand="Made with Dash",
            brand_href="#",
            color=colors['text'],
            style={'width': '100%'},
            dark=True,
            fluid=True

            )],
        no_gutters = False,
        justify = 'right'),
    dbc.Row(children= [
        dbc.Col(children =[
            html.H1('MINUSMA Dashboard', style={'color':'#274472','margin-top':'2vw'}),
            html.A(id = 'output_timer',style={'color':'#274472','margin-bottom':'1vw'})],
                style={'color':colors['text'],
                       'border': '0px solid',
                       'display':'grid',
                       'justify-content':'center',
                       'text-align':'center',
                       'backgroundColor':'white'},
                width=12)
        ]),
    dbc.Row(children=[
        html.H6('UNITED NATIONS MULTIDIMENSIONAL INTEGRATED STABILIZATION MISSION IN MALI',
                style={'font-family':'Courier-New',
                       'font-size':28,
                       'color':colors['text']
                           })],
        style={'backgroundColor':'white',
               'display':'grid',
               'justify-content':'center',
               'text-align':'center'
               }),
    html.Br(),
    dbc.Row(children=[
        dbc.Col(children=[
            dbc.Card(
                dcc.Graph(id='fig_indicator1'),
                body=True,
                color = 'light',      
                style={'display':'grid',
                       'justify-content':'center',
                       'margin-left':'1vw'})]
            ,width=4),
        dbc.Col(children=[
            dbc.Card(
                dcc.Graph(id='fig_indicator2'),
                body=True,
                color = 'light',      
                style={'display':'grid',
                       'justify-content':'center',
                       'margin-left':'0vw'})]
            ,width=4),
        dbc.Col(children=[
            dbc.Card(
                dcc.Graph(id='fig_indicator3'),
                body=True,
                color = 'light',      
                style={'display':'grid',
                       'justify-content':'center',
                       'margin-right':'1vw'})]
            ,width=4),
        
        dbc.Col(children=[
            dcc.Graph()]
            ,width=4)
        
        ])
    

    
    ])
    
@app.callback(
    [Output(component_id='output_timer',component_property='children')],
    [Input(component_id='my_interval',component_property = 'n_intervals')])
def update_time(n):
    time_now = dt.datetime.now(gmt).strftime('%H:%M')
    
    return ('Local Time: ' + str(time_now),)

@app.callback(
    [Output(component_id = 'fig_indicator1', component_property = 'figure'),
     Output(component_id = 'fig_indicator2', component_property = 'figure'),
     Output(component_id = 'fig_indicator3', component_property = 'figure')
     ],
    [Input(component_id='my_interval_graphs',component_property = 'n_intervals')])


def update_graphs(n):
    
    token = 'pk.eyJ1Ijoic21vc2U5NCIsImEiOiJja2N1c2RxbncwbXpzMnNwYmZzeTVjcXY5In0.JCYT6a5J_4IiEeVBoinhvg'
    api = "https://api.acleddata.com/acled/read?terms=accept&country=Mali&iso=466&limit=0"
    AcledData = pd.read_json(api)
    AcledData = pd.DataFrame(AcledData['data'].to_list())
    data = AcledData.to_csv('Processed_Acled_Mali.csv')
    data = pd.read_csv('Processed_Acled_Mali.csv')
    
    years_active = ['2013','2014','2015','2016','2017','2018','2019','2020']
    map_data = pd.DataFrame(data.copy())
    map_data = map_data[map_data['year'].isin(years_active)]
    map_data['year'] = map_data['year'].astype('category')
    map_data['event_date'] = pd.to_datetime(map_data['event_date'])
    cum_sum = pd.DataFrame(map_data.groupby(['admin1'])['fatalities'].sum())
    minusma_frame = map_data[map_data['actor1'].str.contains('MINUSMA')|map_data['actor2'].str.contains("MINUSMA")]
    minusma_frame['value_counts'] = 1
    
    #Set up datetime object to get today's date
    today = pd.Timestamp(dt.date.today())
    start_delta = dt.timedelta(weeks=1)
    last_week = pd.Timestamp(today - start_delta)
    mask = (map_data['event_date'] > last_week) & (map_data['event_date'] <= today)
    week_fatalities = int(map_data.loc[mask]['fatalities'].sum())
    total_fatalities = int(map_data['fatalities'].sum())
    time_now = dt.datetime.now().strftime('%H:%M')
    
    fig_indicator1 = go.Figure()
    fig_indicator1.add_trace(go.Indicator(
        value = total_fatalities,
        title = 'Fatalities since 2013',   
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig_indicator1.update_layout(paper_bgcolor = '#41729F',
                                 font= {'color': 'white'},
                                 height=200,width=400)
    fig_indicator2 = go.Figure()
    fig_indicator2.add_trace(go.Indicator(
        value = week_fatalities,
        title = 'Fatalities in last 7 days',
        mode='number',
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig_indicator2.update_layout(paper_bgcolor = '#274472',
                                 font= {'color': 'white'},
                                 height=200,width=400)
    
    fig_indicator3 = go.Figure()
    fig_indicator3.add_trace(go.Indicator(
        value = int(len(map_data)),
        title = 'Incidents since 2013',
        mode='number',   
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig_indicator3.update_layout(paper_bgcolor = '#5885AF',
                                 font= {'color': 'white'},
                                 height=200,width=400)
    
    return (fig_indicator1,fig_indicator2,fig_indicator3,)

    
if __name__ == '__main__':
    app.run_server(debug=True)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    