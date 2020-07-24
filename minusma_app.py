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
    dbc.Row(html.H2('dfsdf'))
    
    
    
    ],

    
    
    style = {'backgroundColor':'#41729F'})
    
    
    
if __name__ == '__main__':
    app.run_server(debug=True)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    