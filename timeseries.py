# -*- coding: utf-8 -*-
# @Author: Edward-Praveen
# @Date:   2020-05-19 05:57:47
# @Last Modified by:   Edward-Praveen
# @Last Modified time: 2020-05-19 08:43:07


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.express as px
#import folium
import plotly.graph_objects as go
from data_processing import time_series

def timeseries():

    url = 'https://api.covid19india.org/data.json'
    headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    source = requests.get(url,headers=headers)
    req_json = source.json()
    #print(req_json)
    timeseries = req_json['cases_time_series']
    confirmed = []
    deaths = []
    recovered = []
    date = []
    total_confirmed = []
    total_deaths = []
    total_recovered = []

    for cases in timeseries:
        confirmed.append(cases['dailyconfirmed'])
        deaths.append(cases['dailydeceased'])
        recovered.append(cases['dailyrecovered'])
        date.append(cases['date'].strip())
        total_confirmed.append(cases['totalconfirmed'])
        total_deaths.append(cases['totaldeceased'])
        total_recovered.append(cases['totalrecovered'])

    tsdf = pd.DataFrame(list(zip(date,confirmed,deaths,recovered,total_confirmed,total_deaths,total_recovered)),
    columns=['Date','Confirmed','Deaths','Recovered','Total_confirmed','Total_deaths','Total_recovered'])

    cols = ['Confirmed','Deaths','Recovered','Total_confirmed','Total_deaths','Total_recovered']

    for col in cols:
        tsdf[col] = tsdf[col].astype(int)
    
    tsdf['Date'] = tsdf['Date'].map(time_series)
    return tsdf

def ts_graph():

    ts = timeseries()
    fig = go.Figure()

    # Add traces
    fig.add_trace(go.Scatter(
        x = list(ts.Date),
        y = list(ts.Total_confirmed),
        name="Confirmed",
        text = list(ts.Total_confirmed),
        yaxis="y",
    ))

    fig.add_trace(go.Scatter(
        x = list(ts.Date),
        y = list(ts.Total_recovered),
        name="Recovered",
        text=list(ts.Total_recovered),
        yaxis="y2",
    ))

    fig.add_trace(go.Scatter(
        x = list(ts.Date),
        y = list(ts.Total_deaths),
        name="Deceased",
        text = list(ts.Total_deaths),
        yaxis="y3",
    ))



    # style all the traces
    fig.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.5},
        marker={"size": 8},
        mode="lines+markers",
        showlegend=False
    )

    # Add annotations
    fig.update_layout(
        annotations=[
            dict(
                x="2020-02-27",
                y=0,
                arrowcolor="rgba(55, 250, 247, 0.2)",
                arrowsize=0.3,
                ax=0,
                ay=30,
                text="No Lockdown",
                xref="x",
                yanchor="bottom",
                yref="y"
            ),
            dict(
                x="2020-04-01",
                y=0,
                arrowcolor="rgba(63, 81, 181, 0.2)",
                arrowsize=0.3,
                ax=0,
                ay=30,
                text="Phase1",
                xref="x",
                yanchor="bottom",
                yref="y"
            ),
            dict(
                x="2020-04-23",
                y=0,
                arrowcolor="rgba(76, 175, 80, 0.1)",
                arrowsize=0.3,
                ax=0,
                ay=30,
                text="Phase2",
                xref="x",
                yanchor="bottom",
                yref="y"
            ),
            dict(
                x="2020-05-10",
                y=0,
                arrowcolor="rgba(247, 68, 71, 0.1)",
                arrowsize=0.3,
                ax=0,
                ay=30,
                text="Phase3",
                xref="x",
                yanchor="bottom",
                yref="y"
            ),
            dict(
                x="2020-05-25",
                y=0,
                arrowcolor="rgba(229, 4, 229, 0.1)",
                arrowsize=0.3,
                ax=0,
                ay=30,
                text="Phase4",
                xref="x",
                yanchor="bottom",
                yref="y"
            )
        ],
    )

    # Add shapes
    fig.update_layout(
        shapes=[
            dict(
                fillcolor="rgba(55, 250, 247, 0.2)",
                line={"width": 0},
                type="rect",
                x0="2020-01-30",
                x1="2020-03-24",
                xref="x",
                y0=0,
                y1=0.6,
                yref="paper"
            ),
            dict(
                fillcolor="rgba(63, 81, 181, 0.2)",
                line={"width": 0},
                type="rect",
                x0="2020-03-25",
                x1="2020-04-14",
                xref="x",
                y0=0,
                y1=0.6,
                yref="paper"
            ),
            dict(
                fillcolor="rgba(76, 175, 80, 0.1)",
                line={"width": 0},
                type="rect",
                x0="2020-04-15",
                x1="2020-05-03",
                xref="x",
                y0=0,
                y1=0.6,
                yref="paper"
            ),
            dict(
                fillcolor="rgba(247, 68, 71, 0.1)",
                line={"width": 0},
                type="rect",
                x0="2020-05-04",
                x1="2020-05-17",
                xref="x",
                y0=0,
                y1=0.6,
                yref="paper"
            ),
            dict(
                fillcolor="rgba(229, 4, 229, 0.1)",
                line={"width": 0},
                type="rect",
                x0="2020-05-18",
                x1="2020-05-31",
                xref="x",
                y0=0,
                y1=0.6,
                yref="paper"
            )
        ]
    )

    # Update axes
    fig.update_layout(
        xaxis=dict(
            autorange=True,
            range=["2020-01-30", "2020-05-31"],
            rangeslider=dict(
                autorange=True,
                range=["2020-01-30", "2020-05-31"]
            ),
            type="date"
        ),
        yaxis=dict(
            anchor="x",
            autorange=True,
            domain=[0, 0.2],
            linecolor="#673ab7",
            mirror=True,
            range=[-1, 120000],
            showline=True,
            side="right",
            tickfont={"color": "#673ab7"},
            tickmode="auto",
            ticks="",
            titlefont={"color": "#673ab7"},
            type="linear",
            zeroline=False
        ),
        yaxis2=dict(
            anchor="x",
            autorange=True,
            domain=[0.2, 0.4],
            linecolor="#E91E63",
            mirror=True,
            range=[0, 3500],
            showline=True,
            side="right",
            tickfont={"color": "#E91E63"},
            tickmode="auto",
            ticks="",
            titlefont={"color": "#E91E63"},
            type="linear",
            zeroline=False
        ),
        yaxis3=dict(
            anchor="x",
            autorange=True,
            domain=[0.4, 0.6],
            linecolor="#795548",
            mirror=True,
            range=[0, 45000],
            showline=True,
            side="right",
            tickfont={"color": "#795548"},
            tickmode="auto",
            ticks="",
            title="mg/L",
            titlefont={"color": "#795548"},
            type="linear",
            zeroline=False
        )
    )

    # Update layout
    fig.update_layout(
        dragmode="zoom",
        hovermode="x",
        legend=dict(traceorder="reversed"),
        height=600,
        template="plotly_white",
        margin=dict(
            t=100,
            b=100
        ),
    )

    return plotly.offline.plot(fig,output_type='div')
    