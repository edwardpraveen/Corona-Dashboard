# -*- coding: utf-8 -*-
# @Author: Edward-Praveen
# @Date:   2020-05-19 08:43:53
# @Last Modified by:   Edward-Praveen
# @Last Modified time: 2020-05-19 11:02:53

from flask import Flask, render_template, send_file, make_response
from coronaIndia import table, plot1, plot2, plot3, top10, ageWise, malefemaleratio, total
from coronaworld import top20
from timeseries import ts_graph
from flask import *
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
#import folium
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)


@app.route('/')
def show_tables():
    tableDisplay = table()
    figureDisplay1 = plot1()
    figureDisplay2=plot2()
    figureDisplay3=plot3()
    top10fig = top10()
    top20world = top20()
    #bedsLowestCount = bedslowest()
    dateWise = ts_graph()
    ageWiseDate = ageWise()
    maleFemaleRatio = malefemaleratio()
    #icmrdata=icmr()
    totals=total()
    #positives=positive()
    return render_template('index.html',  returnList = tableDisplay, figure1=figureDisplay1, figure2=figureDisplay2,figure3=figureDisplay3,
                    top10list=top10fig, top20list=top20world, dateWiseData=dateWise,
                    ageWiseData=ageWiseDate, maleFemale=maleFemaleRatio, total_data=totals)
    

if __name__ == "__main__":
    app.jinja_env.cache = {}
    app.run(debug=True)