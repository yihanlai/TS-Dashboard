import streamlit as st
from streamlit_echarts import st_echarts

import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from datetime import datetime

# np.random.seed(9999)

def get_line_chart(data, x_axis, y_axis ,title=None):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    lines = (
        alt.Chart(data, title = title)
        .mark_line()
        .encode(
            x = x_axis,
            y = y_axis,
            color="site",
            strokeDash="site",
        )
    )
    points = lines.transform_filter(hover).mark_circle(size=65)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x=x_axis,
            y=y_axis,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(x_axis, title=x_axis),
                alt.Tooltip(y_axis, title=y_axis),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

def get_pie_chart(sizes, labels, colors):
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, 
                autopct='%1.1f%%', 
                wedgeprops = { 'linewidth' : 5, 'edgecolor' : 'white'}, 
                colors = colors, 
                startangle=90)
    return fig

def generate_random_ratio(num):
    list1 = np.random.randint(10, 100, size=num)
    ratio = 100/ sum(list1)
    return list1 / ratio


############# generate fake data #############
fake_storage = np.random.randint(50,200,3)
fake_inventory = np.random.randint(100,500,4)

storage_records = {
    "title": {"text": "倉庫使用率", "subtext":"Storage Utilization", "left": "center"},
    "tooltip": {"trigger": "item"},
    "series": [
        {
            "name": "Storage Utilization",
            "type": "pie",
            "radius": "50%",
            "data": [
                {"value": f"{fake_storage[0]}", "name": "Empty"},
                {"value": f"{fake_storage[1]}", "name": "Reserved"},
                {"value": f"{fake_storage[2]}", "name": "Occupied"},
            ],
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"}
            },
        }
    ],
}

inventory_records = {
    "title": {"text": "庫存類型佔比", "subtext": "Inventory Type","left": "center"},
    "tooltip": {"trigger": "item"},
    "series": [
        {
            "name": "Storage Utilization",
            "type": "pie",
            "radius": "50%",
            "data": [
                {"value": f"{fake_inventory[0]}", "name": "Finished\nProducts"},
                {"value": f"{fake_inventory[1]}", "name": "Semi-Finished\nProducts"},
                {"value": f"{fake_inventory[2]}", "name": "Defective\nProducts"},
                {"value": f"{fake_inventory[3]}", "name": "Raw\nMaterial"},
            ],
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"}
            },
        }
    ],
}

temp_data = {'site': ['新竹1倉']*31 + ['新竹2倉']*31 + ['苗栗1倉']*31,
             'date': np.tile(pd.date_range('2022-12-01','2022-12-31'), 3), 
             'temperature': np.round(np.random.uniform(15,25,31*3), 1),
             }

humid_data = {'site': ['新竹1倉']*31 + ['新竹2倉']*31 + ['苗栗1倉']*31,
              'date': np.tile(pd.date_range('2022-12-01','2022-12-31'), 3), 
              'humidity': np.round(np.random.uniform(15,40,31*3), 1),
              }

####################################################


## dashboard strat
st.set_page_config(layout="wide", page_title="dashboard app")
st.title('倉儲 Dashboard')

## selet sites
col001, col002 =  st.columns(2)
all_sites = np.array(['新竹1倉', '新竹2倉', '苗栗1倉'])
col001.write("#### :house: Please select a warehouse")
col001.write("##### 請選擇欲查詢倉庫")
site = col001.selectbox(" ", all_sites)

## selee date
col002.write("#### :calendar: Please select a date")
col002.write("##### 請選擇欲查詢日期")
date = col002.date_input(" ", datetime.now())

st.write("")

## real-time data visulization
if date:
    real_time_temp = np.random.randint(15,25)
    delta_temp = np.random.randint(-5,5)
    real_time_humid = np.random.randint(15,25)
    delta_humid = np.random.randint(-5,5)
    real_time_inventory_day = np.random.randint(5,15)
    delta_inventory_day = np.random.randint(-5,5)
    real_time_correct_rate = np.random.randint(95,100)
    delta_correct_rate = np.random.randint(-3,5)

st.write(f"#### :bar_chart: Real-time Information of {site}")
st.write(f"##### {site} 即時資料")

col01, col02, col03, col04 = st.columns(4)
### IoT部分
col01.metric("溫度", f"{real_time_temp} °C", f"{delta_temp} °C")
col02.metric("濕度", f"{real_time_humid} %", f"{delta_humid} %")
### 庫存KPI部分
col03.metric("庫存週轉天數", f"{real_time_inventory_day} days", f"{delta_inventory_day}")
col04.metric("進/出貨準確率", f"{real_time_correct_rate} %", f"{delta_correct_rate} %")

st.write("")

## pie chart
col21, col22 = st.columns(2)
with col21:
    st_echarts(options=storage_records, height="400px")
    
with col22:
    st_echarts(options=inventory_records, height="400px")

st.write("")

## line chart
st.write(f"#### :bar_chart:  History Information of {site}")
st.write(f"##### {site} 歷史資料")
st.write("")

col11, col12 = st.columns(2)
temp_df = pd.DataFrame(temp_data)
temp_df = temp_df[temp_df.site == site]
chart = get_line_chart(temp_df, "date", "temperature", "12月每日平均溫度")
col11.altair_chart(chart, use_container_width=True)

humid_df = pd.DataFrame(humid_data)
humid_df = humid_df[humid_df.site == site]
chart = get_line_chart(humid_df, "date", "humidity", "12月每日平均濕度")
col12.altair_chart(chart, use_container_width=True)
