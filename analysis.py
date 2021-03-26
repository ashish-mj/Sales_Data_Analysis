#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 14:55:58 2021

@author: ashish
"""

import pandas as pd
import os
import matplotlib.pyplot as plt


files = [file for file in os.listdir("./Sales_Data/")]
all_months_data = pd.DataFrame()


for file in files:
    month_data = pd.read_csv("./Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data, month_data])
    
all_months_data.to_csv("./Sales_Data/data.csv", index=False)
data = pd.read_csv("./Sales_Data/data.csv")

data = data[data["Order Date"].str[0:2] !='Or']
data = data.dropna(how='all')
data["Month"] = data["Order Date"].str[0:2]
data["Month"] = data["Month"].astype('int32')
data["Quantity Ordered"] = pd.to_numeric(data["Quantity Ordered"])
data["Price Each"] = pd.to_numeric(data["Price Each"])

'''
nan_data = data[data.isna().any(axis=1)]
print(nan_data.head())
'''

#highest and lowest sales in the month

data["Sales"] = data["Quantity Ordered"] * data["Price Each"]
sales_month = data.groupby('Month').sum()["Sales"]
month = range(1,13)
plt.bar(month,sales_month)
plt.show()

