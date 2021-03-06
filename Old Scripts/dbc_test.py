#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 14:03:48 2020

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

app = dash.Dash(__name__)
server = app.server


colors = {
    'background': 'rgb(240,240,230)',
    'text': 'rgb(0, 118, 192)'
}
###PROCESSING THE DATA
def process_Acled_data():
    api = "https://api.acleddata.com/acled/read?terms=accept&country=Mali&iso=466&limit=0"

    AcledData = pd.read_json(api)

    AcledData = pd.DataFrame(AcledData['data'].to_list())
    data = AcledData.to_csv('Processed_Acled_Mali.csv')
    data = pd.read_csv('Processed_Acled_Mali.csv')
    return data

data = process_Acled_data()

years_active = ['2013','2014','2015','2016','2017','2018','2019','2020']
map_data = data.drop('Unnamed: 0',axis=1)
map_data = map_data[map_data['year'].isin(years_active)]
map_data['year'] = map_data['year'].astype('category')
map_data['event_date'] = pd.to_datetime(map_data['event_date'])
cum_sum = pd.DataFrame(map_data.groupby(['admin1']).sum())

#Set up datetime object to get today's date
today = pd.Timestamp(dt.date.today())
start_delta = dt.timedelta(weeks=2)
last_week = pd.Timestamp(today - start_delta)
mask = (map_data['event_date'] > last_week) & (map_data['event_date'] <= today)
week_fatalities = int(map_data.loc[mask]['fatalities'].sum())
total_fatalities = int(map_data['fatalities'].sum())
time_now = dt.datetime.now().strftime('%H:%M')

###GENERATING THE FIGURES FOR PLOTTING
fig = px.scatter_geo(map_data, 
                     lat = map_data['latitude'],
                     lon = map_data['longitude'],
                     color = map_data['year'],
                     center=dict(
                         lon=map_data.loc[0]['longitude'],
                         lat=map_data.loc[0]['latitude']),
                     width = 600, height = 600, 
                     title = 'Violence in Mali',
                     hover_data=['actor1'])
                     
fig = fig.update_geos(fitbounds="locations",
                      scope='africa',
                      showcountries=True,
                      showsubunits=True)

fig2 = px.bar(cum_sum,x=map_data['admin1'],y=map_data['fatalities'],
              title = 'Fatalities by Region',
              template='plotly_white')
fig2.update_layout(xaxis_title="Total Fatalities",
                   yaxis_title="Administrative Regions")
fig2.update_traces(marker_color = 'rgb(0,118,192)')

fig_indicator1 = go.Figure()
fig_indicator1.add_trace(go.Indicator(
    value = total_fatalities,
    title = 'Fatalities since 2013',   
    domain = {'x': [0, 1], 'y': [0, 1]}))
fig_indicator1.update_layout(paper_bgcolor = colors['text'],
                             font= {'color': 'white'},
                             height=250)


fig_indicator2 = go.Figure()
fig_indicator2.add_trace(go.Indicator(
    value = week_fatalities,
    title = 'Fatalities this week',
    mode='number',
    domain = {'x': [0, 1], 'y': [0, 1]}))
fig_indicator2.update_layout(paper_bgcolor = colors['text'],
                             font= {'color': 'white'},
                             height=250)

fig_indicator3 = go.Figure()
fig_indicator3.add_trace(go.Indicator(
    value = int(len(map_data)),
    title = 'Incidents since 2013',
    mode='number',   
    domain = {'x': [0, 1], 'y': [0, 1]}))
fig_indicator3.update_layout(paper_bgcolor = colors['text'],
                             font= {'color': 'white'},
                             height=250)



###HTML AND LAYOUT
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(id = 'live-updating-figures',children=[
    
    dcc.Interval(
            id='my_interval',
            disabled=False,     #if True, the counter will no longer update
            interval=1*8640,#increment the counter n_intervals every interval milliseconds
            n_intervals=0,      #number of times the interval has passed
            max_intervals=1,    #number of times the interval will be fired.
                                #if -1, then the interval has no limit (the default)
                                #and if 0 then the interval stops running.
                                ),
 
    dbc.Row(children = [
        
        dbc.Col(children = [
            html.Img(src=app.get_asset_url('minusma-logo-1.png'),
                     width= '120px',
                     style={'display': 'inline-block'}),
            
            html.H6('UNITED NATIONS MULTIDIMENSIONAL INTEGRATED STABILIZATION MISSION IN MALI',
                    style={
                           'text-align':'left',
                           'margin-top':'2vw'
                           })],
                style={'color':colors['text'],
                       'font-family':'Courier New',
                       'border': '1px solid',
                        'columnCount': 2}, 
                width=3,
                align='center'),
        
        dbc.Col(children = [
            html.H1('MINUSMA Dashboard', style={'color':'Black','margin-top':'3vw'}),
            html.A('Local Time: ' + str(time_now),style={'color':'Black','margin-bottom':'1vw'})],
                style={'color':colors['text'],
                       'border': '1px solid',
                       'display':'grid',
                       'justify-content':'center',
                       'text-align':'center',
                       'backgroundColor':'white'},
                width=6),
        
        dbc.Col(children =[
            html.Br(),
            html.A('United Nations Peacekeeping',
                   href='https://peacekeeping.un.org/en',
                   style={'color':'Black'}),
            html.Br(),
            html.A('Made using Acled data',
                   href='https://acleddata.com/#/dashboard',
                   style={'color':'Black'}),
            html.Br(),
            html.A('Project Github',
                   href='www.github.com/smose94',
                   style={'color':'Black'}),
            html.Br(),
            html.A('MINUSMA Home',
                   href='https://minusma.unmissions.org/en',
                   style={'color':'Black'})
            
            ],
                style={'color':colors['text'],
                       'border':'1px solid'},
                width=3)
        ]),
    dbc.Row(children=[
        dbc.Col(children=[
            dcc.Graph(figure=fig_indicator1)],width=4),
        dbc.Col(children = [
            dcc.Graph(figure=fig_indicator2)],width=4),
        dbc.Col(children = [
            dcc.Graph(figure=fig_indicator3)],width=4),
     
        
        ],
        style={'color':colors['text'],
               'border':'1px solid',
               'backgroundColor':colors['text']}),
    
    dbc.Row(children=[
        dbc.Col(
            dcc.Graph(figure=fig),width=6),
        dbc.Col(
            dcc.Graph(figure=fig2),width=6,style={'margin-top':'8vw'})
        ])

        
        
        ])

###RUN THE APP
if __name__ == '__main__':
    app.run_server(debug=True)












