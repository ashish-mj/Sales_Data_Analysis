#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 14:55:58 2021

@author: ashish
"""

import pandas as pd
import os


files = [file for file in os.listdir("./Sales_Data/")]
all_months_data = pd.DataFrame()


for file in files:
    month_data = pd.read_csv("./Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data, month_data])
    
all_months_data.to_csv("./Sales_Data/data.csv", index=False)
data = pd.read_csv("./Sales_Data/data.csv")
print(data.head())
print(data.tail())