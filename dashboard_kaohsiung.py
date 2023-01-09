import random
import streamlit as st
from streamlit_echarts import st_echarts

import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from datetime import datetime

np.random.seed(9999)

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


@st.cache()
def generate_random_realtime_data(site, date):
    real_time_temp = random.randint(15,25)
    delta_temp = random.randint(-5,5)
    real_time_humid = random.randint(15,25)
    delta_humid = random.randint(-5,5)
    real_time_inventory_day = random.randint(5,15)
    delta_inventory_day = random.randint(-5,5)
    real_time_correct_rate = random.randint(95,100)
    delta_correct_rate = random.randint(-3,5)

    real_time_data = [real_time_temp, delta_temp, real_time_humid, delta_humid,
                      real_time_inventory_day, delta_inventory_day, real_time_correct_rate, delta_correct_rate]

    fake_storage = [random.randint(50,200) for x in range(0,4)]
    fake_inventory = [random.randint(100,500) for x in range(0,5)]


    return real_time_data, fake_storage, fake_inventory


## dashboard strat
st.set_page_config(layout="wide", page_title="dashboard app")
st.markdown(" <style>iframe{ height: 400px !important } ", unsafe_allow_html=True) # Edit by Tim
st.title('倉儲 Dashboard')

## selet site
col001, col002 =  st.columns(2)
all_sites = np.array(['台北倉', '桃園倉', '高雄倉'])
col001.write("#### :house: Please select a warehouse")
col001.write("##### 請選擇欲查詢倉庫")
site = col001.selectbox(" ", all_sites, index = 2)

## selee date
col002.write("#### :calendar: Please select a date")
col002.write("##### 請選擇欲查詢日期")
date = col002.date_input(" ", datetime.now())

st.write("")

real_time_data, fake_storage, fake_inventory = generate_random_realtime_data(site, date)

######################################## generate fake data ########################################
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

temp_data = {'site': ['台北倉']*31 + ['桃園倉']*31 + ['高雄倉']*31,
             'date': np.tile(pd.date_range('2022-12-01','2022-12-31'), 3), 
             'temperature': np.round(np.random.uniform(15,25,31*3), 1),
             }

humid_data = {'site': ['台北倉']*31 + ['桃園倉']*31 + ['高雄倉']*31,
              'date': np.tile(pd.date_range('2022-12-01','2022-12-31'), 3), 
              'humidity': np.round(np.random.uniform(15,40,31*3), 1),
              }
####################################################################################################


## real-time data visulization
st.write(f"#### :bar_chart: Real-time Information of {site}")
st.write(f"##### {site} 即時資料")

col01, col02, col03, col04 = st.columns(4)
### IoT部分
col01.metric("溫度", f"{real_time_data[0]} °C", f"{real_time_data[1]} °C")
col02.metric("濕度", f"{real_time_data[2]} %", f"{real_time_data[3]} %")
### 庫存KPI部分
col03.metric("庫存週轉天數", f"{real_time_data[4]} days", f"{real_time_data[5]}")
col04.metric("進/出貨準確率", f"{real_time_data[6]} %", f"{real_time_data[7]} %")

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

st.write("")

# Edit by Tim
## lot selection and search
def randomtimes(start, end, frmt="%Y-%m-%d %H:%M:%S"):
    stime = datetime.strptime(start, frmt)
    etime = datetime.strptime(end, frmt)
    random_time = random.random() * (etime - stime) + stime
    return random_time.strftime(frmt)
    
@st.cache()
def create_fake_lot_detail():
    fake_lot_detail = [[[] for i in range(6)] for i in range(5)] 

    for i in range(5):
        for j in range(6):
            mtrlNum = "W" + str(random.randrange(2000000, 3000000))
            num = random.randrange(0, 10000)
            remainNum = 10000 - num
            fake_lot_detail[i][j].append(chr(i+65))
            fake_lot_detail[i][j].append("0" + str(j))
            fake_lot_detail[i][j].append(str(mtrlNum))
            fake_lot_detail[i][j].append(str(num))
            fake_lot_detail[i][j].append(str(remainNum))
            fake_lot_detail[i][j].append(randomtimes("2023-01-02 00:00:00", "2023-01-10 23:59:59"))
            fake_lot_detail[i][j].append([random.randrange(0, 10000) for i in range(7)])
            fake_lot_detail[i][j].append([random.randrange(0, 10000) for i in range(12)])

    return fake_lot_detail

def search_lot_detail(option1, option2, fake_lot_detail):
    with col13:
        search_lot_str = option1 + "-" + option2
        i = ord(option1)-65
        j = int(option2[1])-1
        
        #lot detail
        st.write("---")
        st.write(f"##### {search_lot_str} 儲格資訊：")
        st.write(f"###### 產品編號：{fake_lot_detail[i][j][2]}")
        st.write(f"###### 目前儲存量：{fake_lot_detail[i][j][3]}")
        st.write(f"###### 剩餘儲存量：{fake_lot_detail[i][j][4]}")
        st.write(f"###### 入庫時間：{fake_lot_detail[i][j][5]}")

        # lot detail graph
        st.write("---")
        st.write(f"##### {search_lot_str} 儲格儲存量變動")
        tab1, tab2 = st.tabs(["Day", "Month"])
        
        with tab1:
            reload_lot_graph(i, j, fake_lot_detail, "week")

        with tab2:
            reload_lot_graph(i, j, fake_lot_detail, "month")

def reload_lot_graph(i, j, fake_lot_detail, frmt):
    if (frmt == "week"):
        option = {
            "xAxis": {
                "type": "category",
                "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            },
            "yAxis": {"type": "value"},
            "series": [{"data": fake_lot_detail[i][j][6], "type": "line"}],
        }
        st_echarts(
            options=option, height="400px", width="400px", key = "week_graph"
        )
    elif (frmt == "month"):
        option = {
            "xAxis": {
                "type": "category",
                "data": ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"],
            },
            "yAxis": {"type": "value"},
            "series": [{"data": fake_lot_detail[i][j][7], "type": "line"}],
        }
        st_echarts(
            options=option, height="400px", width="400px", key = "month_graph"
        )

st.write(f"#### :bar_chart:  Lot Information of {site}")
st.write(f"##### 請選擇欲查詢儲格")
col13, col14 = st.columns([1,1])
fake_lot_detail = create_fake_lot_detail() # ["A", "01", "mtrlNum", num, remainNum, "2023-01-02 17:08:02"]

with col13:
    option1 = st.selectbox(
        "",
        ("A", "B", "C", "D", "E"),
        index=0,
        label_visibility="collapsed"
    )
    option2 = st.selectbox(
        "",
        ("01", "02", "03", "04", "05", "06"),
        index=0,
        label_visibility="collapsed"
    )
    button_search = st.button('Search', type="primary", on_click=search_lot_detail, args=(option1, option2, fake_lot_detail))

with col14:
    st.write("---")
    st.write(f"##### {site} 各儲格目前儲存量")

    option1 = ["A", "B", "C", "D", "E"]
    option2 = ["01", "02", "03", "04", "05", "06"]
    data = []
    for i in range(5):
        for j in range(6):
            data.append([i, j, fake_lot_detail[i][j][3]])

    data = [[d[1], d[0], d[2] if d[2] != 0 else "-"] for d in data]

    option = {
        "tooltip": {"position": "top"},
        "grid": {"height": "50%", "top": "10%"},
        "xAxis": {"type": "category", "data": option2, "splitArea": {"show": True}},
        "yAxis": {"type": "category", "data": option1, "splitArea": {"show": True}},
        "visualMap": {
            "min": 0,
            "max": 10000,
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "bottom": "15%",
        },
        "series": [
            {
                "name": "Punch Card",
                "type": "heatmap",
                "data": data,
                "label": {"show": True},
                "emphasis": {
                    "itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0, 0, 0, 0.5)"}
                },
            }
        ],
    }
    st_echarts(option, height="400px")