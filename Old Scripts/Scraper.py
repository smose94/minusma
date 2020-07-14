#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 20:49:57 2020

@author: simon
"""


import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

import pandas as pd

api = "https://api.acleddata.com/acled/read?terms=accept&country=Mali&iso=466&limit=0"

AcledData = pd.read_json(api)

AcledData = pd.DataFrame(AcledData['data'].to_list())

AcledData.to_csv('Processed_Acled_Mali.csv')