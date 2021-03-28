#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 14:55:58 2021

@author: ashish
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

'''
files = [file for file in os.listdir("./Sales_Data/")]
all_months_data = pd.DataFrame()


for file in files:
    month_data = pd.read_csv("./Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data, month_data])
    
all_months_data.to_csv("./Sales_Data/data.csv", index=False)
'''



data = pd.read_csv("../data.csv")

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
plt.xticks(month,rotation='vertical',size=8)
plt.xlabel("Month")
plt.ylabel("Sales in USD $")
plt.show()


#City which had highest number of sales

data["City"]=data["Purchase Address"].apply(lambda x: x.split(",")[1]+" "+x.split(",")[2].split(" ")[1])
sales_cities = data.groupby('City').sum()
print(sales_cities.head())
cities= [city for city ,_ in data.groupby("City")]
plt.bar(cities,sales_cities["Sales"])
plt.xticks(cities,rotation='vertical',size=8)
plt.xlabel("Cities")
plt.ylabel("Sales in USD $")
plt.show()


#When to advertise

data["Order Date"] = pd.to_datetime(data["Order Date"])
data["Hour"] = data["Order Date"].dt.hour
data["Minute"] = data["Order Date"].dt.minute
hours = [hour for hour, _ in data.groupby('Hour')]
plt.plot(hours,data.groupby(['Hour']).count())
plt.xticks(hours)
plt.grid()
plt.xlabel("Hour")
plt.ylabel("Sales count")
plt.show()


#products often brought together

products = data[data["Order ID"].duplicated(keep=False)]
products["Grouped"] = products.groupby("Order ID")["Product"].transform(lambda x : ",".join(x))
products = products[["Order ID","Grouped"]].drop_duplicates()

count=Counter()
for row in products["Grouped"]:
    row_list = row.split(",")
    count.update(Counter(combinations(row_list,3)))
    
for key,value in count.most_common(10):
    print(key,value)


#product sold the most
    
product_group = data.groupby("Product")
quantity_order = product_group.sum()["Quantity Ordered"]
prices = data.groupby("Product").mean()["Price Each"]

print(prices.head())
products = [product for product, _ in product_group ]

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products,quantity_order,color='g')
ax2.plot(products, prices, 'b-')
ax1.set_xlabel("Product")
ax1.set_ylabel("Sales count", color='g')
ax2.set_ylabel('Prices', color='b')
ax1.set_xticklabels(products,rotation='vertical',size=8)
plt.show()



