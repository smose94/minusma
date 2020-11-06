#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 19:52:34 2020

@author: simon
"""
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import datetime as dt
from datetime import date, timedelta
from pytz import timezone
gmt = timezone('GMT')
import json
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import config 

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
        no_gutters = True,
        justify = 'right'),

    dbc.Row(children = [
        
        dbc.Col(children =[
            html.Img(src=app.get_asset_url('minusma-logo-1.png'),
                     width= '120px'
                     )],
                style={'color':colors['text'],
                       'display':'grid',
                       'border':'1px solid',
                       'font-family':'Courier New',
                       'columnCount': 1,
                       'justify-content':'center'
                       },
                width=3),
                
        dbc.Col(children = [
            html.H1('MINUSMA Dashboard', style={'color':'#274472','margin-top':'1vw'}),
            html.A(id = 'output_timer',style={'color':'Black','margin-bottom':'0vw'}),
            html.A(id = 'last_update',style={'color':'Black','margin-bottom':'0vw'})],
                style={'color':colors['text'],
                       'border': '1px solid',
                       'display':'grid',
                       'justify-content':'center',
                       'text-align':'center',
                       'backgroundColor':'white'},
                width=6),
        
        dbc.Col(children =[
            html.H6('UNITED NATIONS MULTIDIMENSIONAL INTEGRATED STABILIZATION MISSION IN MALI',
                    style={
                           'text-align':'left',
                           'margin-top':'1.5vw',
                           'font-size':22
                           })],

                style={'color':colors['text'],
                       'border':'1px solid',
                       'font-family':'Courier New',
                       'columnCount': 1
                       },
                width=3)
        ]),
    
        dbc.Row(children=[
        dbc.Col(children=[
            dcc.Graph(id='fig_indicator1')],width=4),
        dbc.Col(children = [
            dcc.Graph(id='fig_indicator2')],width=4),
        dbc.Col(children = [
            dcc.Graph(id='fig_indicator3')],width=4),
        
        ],
        style={'color': 'white',
               'border':'50px solid',
               'backgroundColor':'white',
               'border-color':'white'
               }),
        
    dbc.Row(children = [
        dbc.Col(
            dcc.Graph(id='fig_density_series'),width=4,style={'margin-top':'1vw'}),        
        dbc.Col(
            dcc.Graph(id='fig_minusma_series'),width=4,style={'margin-top':'1vw'}),
        dbc.Col(
            dcc.Graph(id='fig2'),width=4)
        
        ]),
    
    
    dbc.Row(children=[
        dbc.Col(
            dcc.Graph(id='fig'),width=8),
        dbc.Col(children = [
            html.Br(),
            dbc.Row(
                html.H3('',style={'color':colors['text']})
                ),
            dbc.Row(
                dcc.Graph(id='fig_month_incidents',style={"width": "100%","display": "inline-block" })),
            dbc.Row(
                dcc.Graph(id='fig_month_deaths',style={'margin-left':'0vw',"width": "100%","display": "inline" }))
            
            ],width=4, style={'margin-top': '2vw'}
            )
        ]),
    dbc.Row(children=[
        dbc.Col(children=[
            dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H1("", className="display-3"),
                html.P(
                    "",
                    className="lead",
                ),
                html.P(
                    '© Simon Moseley 2020',
                    className="lead"
                ),
            ],
            fluid=True,
            id='jumbotron'
        )
    ],
    
    fluid=True

    )],
            width=12)
        
        ])
    ])

          
@app.callback(
    [Output(component_id='output_timer',component_property='children')],
    [Input(component_id='my_interval',component_property = 'n_intervals')])
def update_time(n):
    time_now = dt.datetime.now(gmt).strftime('%H:%M')
    
    return ('Local Time: ' + str(time_now),)

@app.callback(
    [Output(component_id = 'fig', component_property = 'figure'),
     Output(component_id = 'fig2', component_property = 'figure'),
     Output(component_id = 'fig_density_series', component_property = 'figure'),
     Output(component_id = 'fig_minusma_series', component_property = 'figure'),
     Output(component_id = 'fig_indicator1', component_property = 'figure'),
     Output(component_id = 'fig_indicator2', component_property = 'figure'),
     Output(component_id = 'fig_indicator3', component_property = 'figure'),
     Output(component_id = 'last_update', component_property = 'children'),
     Output(component_id = 'fig_month_incidents', component_property= 'figure'),
     Output(component_id = 'fig_month_deaths', component_property= 'figure'),
     ],
    [Input(component_id='my_interval_graphs',component_property = 'n_intervals')])

def update_graphs(n):
    token = config.token_mapbox   
    api = config.api_key
    AcledData = json.loads(requests.get(api).text)
    AcledData = pd.DataFrame(AcledData['data'])
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
    
    #Get last event in the database
    updated_acled = max(AcledData['event_date'])
    
    #Process the dataframes for the monthly year-on-year comparisons
    last_day_of_prev_month = pd.Timestamp.today().replace(day=1) - timedelta(days=1)
    start_day_of_prev_month = pd.Timestamp.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)
    last_day_last_year = last_day_of_prev_month - timedelta(days=365)
    first_day_last_year = start_day_of_prev_month - timedelta(days=365)
    
    mask_monthly = (map_data['event_date'] > start_day_of_prev_month) & (map_data['event_date'] <=last_day_of_prev_month)
    deaths_last_month = map_data.loc[mask_monthly]['fatalities'].sum()
    incidents_last_month = int(len(map_data.loc[mask_monthly]))
    
    mask_month_year_ago = (map_data['event_date'] > first_day_last_year) & (map_data['event_date'] <= last_day_last_year)
    deaths_month_year_ago = map_data.loc[mask_month_year_ago]['fatalities'].sum()
    incidents_last_month_year_ago = int(len(map_data.loc[mask_month_year_ago]))
    # For printing results
    #print("First day of prev month:", start_day_of_prev_month)
    #print("Last day of prev month:", last_day_of_prev_month)
    
    
    
    
    fig_density_series = px.histogram(map_data,
                                      x = map_data['event_date'],
                                      y=map_data['fatalities'],
                                      template='plotly_white'
                                      )
    fig_density_series.update_traces(marker_color = '#5885AF',opacity=0.7)
    fig_density_series.update_layout(xaxis_title="Time",
                       yaxis_title="Fatalities",
                       title = 'Fatalities by Time'
                         )
    fig_minusma_series = px.histogram(minusma_frame,
                                 x = minusma_frame['event_date'],
                                 y = minusma_frame['value_counts'],
                                 template='plotly_white'
                                 )
    fig_minusma_series.update_traces(marker_color = colors['text'],
                                     opacity=0.7)
    fig_minusma_series.update_layout(xaxis_title="Time",
                       yaxis_title="Events invovling MINUSMA",
                       title = 'Involvement of MINUSMA by Time',
                       paper_bgcolor = 'white'
                         )
       
    fig = px.scatter_mapbox(map_data, 
                     lat = map_data['latitude'],
                     lon = map_data['longitude'],
                     color = map_data['year'],
                     center=dict(
                         lon=-4.0,
                         lat=15.5),
                     width = 900, height = 700, zoom=4, 
                     title = 'Violence in Mali',
                     hover_data= ['actor1'])
    
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)

    
    fig2 = px.bar(cum_sum,x=cum_sum.index.to_list(),y=cum_sum['fatalities'],
              title = 'Fatalities by Region',
              text = cum_sum['fatalities'],
              template='plotly_white')
    fig2.update_layout(xaxis_title="Total Fatalities",
                       yaxis_title="Administrative Regions"
                         )
    fig2.update_traces(marker_color = '#274472',opacity=0.7)
    
    fig_indicator1 = go.Figure()
    fig_indicator1.add_trace(go.Indicator(
        value = total_fatalities,
        title = 'Fatalities since 2013',   
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig_indicator1.update_layout(paper_bgcolor = '#41729F',
                                 font= {'color': 'white'},
                                 height=250)
                                 
                                 
    
    
    fig_indicator2 = go.Figure()
    fig_indicator2.add_trace(go.Indicator(
        value = week_fatalities,
        title = 'Fatalities in last 7 days',
        mode='number',
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig_indicator2.update_layout(paper_bgcolor = '#274472',
                                 font= {'color': 'white'},
                                 height=250)
    
    fig_indicator3 = go.Figure()
    fig_indicator3.add_trace(go.Indicator(
        value = int(len(map_data)),
        title = 'Incidents since 2013',
        mode='number',   
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig_indicator3.update_layout(paper_bgcolor = '#5885AF',
                                 font= {'color': 'white'},
                                 height=250)
    
    fig_month_incidents = go.Figure()
    fig_month_incidents.add_trace(go.Indicator(
        value = int(incidents_last_month),
        title = 'Incidents last month',
        mode = 'number+delta',
        delta = {'reference': incidents_last_month_year_ago, 'increasing':{'color':'red'}, 'decreasing':{'color':'green'}}))
    fig_month_incidents.update_layout(height=250)
    
    fig_months_deaths = go.Figure()
    fig_months_deaths.add_trace(go.Indicator(
        value = int(deaths_last_month),
        title = 'Fatalities last month',
        mode = 'number+delta',
        delta = {'reference': deaths_month_year_ago,'increasing':{'color':'red'},'decreasing':{'color':'green'}},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig_months_deaths.update_layout(height=250)
    
    


    
    return (
            fig,fig2,
            fig_density_series,fig_minusma_series,
            fig_indicator1,fig_indicator2,fig_indicator3,
            'Latest data: ' + str(updated_acled),
            fig_month_incidents, fig_months_deaths,
            )

if __name__ == '__main__':
    app.run_server(debug=True)

