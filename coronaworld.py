# -*- coding: utf-8 -*-
# @Author: Edward-Praveen
# @Date:   2020-05-18 06:09:08
# @Last Modified by:   Edward-Praveen
# @Last Modified time: 2020-05-19 09:57:57

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.express as px
#import folium
import plotly.graph_objects as go
from data_processing import plus_comma


def world_scrap():
    url = 'https://www.worldometers.info/coronavirus/'
    headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    source = requests.get(url, headers = headers)
    soup = BeautifulSoup(source.content,'html.parser')
    world_table = soup.find_all('table')
    world = world_table[0]
    country = []
    total_cases = []
    new_cases = []
    total_deaths = []
    new_deaths = []
    recovered = []
    active_cases = []
    rows = world.find_all('tr')[9:-8] #removing irrelevant columns, tr - parent class table
    for row in rows:
        col = row.find_all('td')
        country.append(col[1].text.strip())
        total_cases.append(col[2].text.strip())
        new_cases.append(col[3].text.strip())
        total_deaths.append(col[4].text.strip())
        new_deaths.append(col[5].text.strip())
        recovered.append(col[6].text.strip())
        active_cases.append(col[7].text.strip())
    dfw = pd.DataFrame(list(zip(country,total_cases,new_cases,total_deaths,new_deaths,recovered,active_cases)),
                        columns=['Country','Total_cases','New_cases','Total_deaths','New_deaths','Recovered','Active_cases'])
    dfw.replace(r'^\s*$',np.nan,regex=True, inplace=True)
    for col in dfw.columns:
        dfw[col] = dfw[col].replace({np.nan:0}) #replacing NaN values with zero
    for name in ['Recovered','Active_cases']:
        dfw[name].loc[dfw[name]=='N/A'] = 0 #replacing N/A values with zero
    
    #removing symbols from dataset
    dfw['New_cases'] = dfw['New_cases'].map(plus_comma)
    dfw['New_deaths'] = dfw['New_deaths'].map(plus_comma)
    dfw['Total_cases'] = dfw['Total_cases'].map(plus_comma)
    dfw['Total_deaths'] = dfw['Total_deaths'].map(plus_comma)
    dfw['Recovered'] = dfw['Recovered'].map(plus_comma)
    dfw['Active_cases'] = dfw['Active_cases'].map(plus_comma)

    #Removing unwanted columns
    dfw['Total_deaths'] = dfw['Total_deaths'] + dfw['New_deaths']
    dfw['Active_cases'] = dfw['Active_cases'] + dfw['New_cases']
    dfw.drop(['New_deaths','New_cases'],axis=1,inplace=True)
    dfw['Total_cases'] = dfw['Recovered'] + dfw['Total_deaths'] + dfw['Active_cases']
    return dfw

def top20():
    df=world_scrap()
    df_latest=df.sort_values("Total_cases", ascending=False)
    df_latest.reset_index(drop=True,inplace=True)

    data=df_latest.iloc[0:20,:]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=data["Country"],
                    y=data["Total_cases"],
                    name='Total Cases',
                    marker_color='indianred'
                    ))
    fig.add_trace(go.Bar(x=data["Country"],
                    y=data["Total_deaths"],
                    name='Deaths',
                    marker_color='lightsalmon'
                    ))

    fig.update_layout(
        title='Cases v/s Deaths ratio in top 20 Countries',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Number of cases',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor="rgba(255, 255, 255, 0)",
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    return plotly.offline.plot(fig,output_type='div')


    
   
