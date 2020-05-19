# -*- coding: utf-8 -*-
# @Author: Edward-Praveen
# @Date:   2020-05-18 06:28:58
# @Last Modified by:   Edward-Praveen
# @Last Modified time: 2020-05-19 10:07:34
import pandas as pd
import numpy as np
import datetime


def plus_comma(num):
    reg = str(num).replace('+','').replace(',','')
    reg1 = int(reg)
    return reg1
    
def time_series(values):
    values = values + ' 2020'    
    s = datetime.datetime.strptime(values,'%d %B %Y')    
    return s 
