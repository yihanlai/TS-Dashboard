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
st.title('倉儲 Dashboard')

## selet site
col001, col002 =  st.columns(2)
all_sites = np.array(['台北倉', '桃園倉', '高雄倉'])
col001.write("#### :house: Please select a warehouse")
col001.write("##### 請選擇欲查詢倉庫")
site = col001.selectbox(" ", all_sites, index = 0)

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



## lot selection and search

st.write(f"#### :bar_chart:  Lot Information of {site}")
st.write(f"##### 請選擇欲查詢儲格")
st.write("")

col13, col14, col15, col16, col17, col18, col19= st.columns([1, 1, 1, 1, 1, 0.5, 5])
parent_state_names = ["a", "b", "c", "d", "e"]
child_state_names = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]

def search_lot_detail():
    st.session_state["type_search"] = "primary"
    search_lot_str = st.session_state.get("parent_selected", "a").upper() + "-" + st.session_state.get("child_selected")
    mtrlnum = "W" + str(random.randrange(2000000, 3000000))
    number = random.randrange(1000, 10000)
    status = random.choice(["S", "F", "V"])
    col19.write(f"#### {search_lot_str} 儲格資訊：")
    col19.write("---")
    col19.write(f"##### 產品編號：{mtrlnum}")
    col19.write(f"##### 數量：{number}")
    col19.write(f"##### 入庫日期：2023-01-02")
    col19.write(f"##### 狀態：{status}")
    reload_number_in_lot()
    

def disable_other_parent(state_name_i):
    for state_name in parent_state_names:
        the_disabled = "disabled_" + state_name
        the_type = "type_" + state_name
        if (state_name == state_name_i):
            st.session_state[the_disabled] = False 
            st.session_state[the_type] = "primary"
            st.session_state["parent_selected"] = state_name
        else:    
            st.session_state[the_type] = "secondary"
        #    st.session_state[the_disabled] = True

    for state_name in child_state_names:
        the_disabled = "disabled_" + state_name
        the_type = "type_" + state_name
        st.session_state[the_disabled] = False
        st.session_state[the_type] = "secondary"
      
    st.session_state["disabled_search"] = True


def disable_other_child(state_name_i):
    st.session_state["type_search"] = "secondary"

    for state_name in child_state_names:
        the_disabled = "disabled_" + state_name
        the_type = "type_" + state_name
        if (state_name == state_name_i):
            st.session_state[the_disabled] = False
            st.session_state[the_type] = "primary"
            st.session_state["child_selected"] = state_name
        else:
            st.session_state[the_type] = "secondary"
        #    st.session_state[the_disabled] = True
    
    st.session_state["disabled_search"] = False


with col13:
    button_a = st.button('A', key='but_a', type=st.session_state.get("type_a", "primary"), on_click=disable_other_parent, args=("a",), disabled=st.session_state.get("disabled_a", False))
    st.write("---")
    button_01 = st.button('01', key='but_01', type=st.session_state.get("type_01", "secondary"), on_click=disable_other_child, args=("01",), disabled=st.session_state.get("disabled_01", False))
    button_02 = st.button('02', key='but_02', type=st.session_state.get("type_02", "secondary"), on_click=disable_other_child, args=("02",), disabled=st.session_state.get("disabled_02", False))
    button_03 = st.button('03', key='but_03', type=st.session_state.get("type_03", "secondary"), on_click=disable_other_child, args=("03",), disabled=st.session_state.get("disabled_03", False))
    st.write("---")
    button_search = st.button('Search', key='but_search_lot_detail', type=st.session_state.get("type_search", "secondary"), on_click=search_lot_detail, disabled=st.session_state.get("disabled_search", True))

with col14:
    button_b = st.button('B', key='but_b', type=st.session_state.get("type_b", "secondary"), on_click=disable_other_parent, args=("b",), disabled=st.session_state.get("disabled_b", False))
    st.write("---")
    button_04 = st.button('04', key='but_04', type=st.session_state.get("type_04", "secondary"), on_click=disable_other_child, args=("04",), disabled=st.session_state.get("disabled_04", False))
    button_05 = st.button('05', key='but_05', type=st.session_state.get("type_05", "secondary"), on_click=disable_other_child, args=("05",), disabled=st.session_state.get("disabled_05", False))
    button_06 = st.button('06', key='but_06', type=st.session_state.get("type_06", "secondary"), on_click=disable_other_child, args=("06",), disabled=st.session_state.get("disabled_06", False))


with col15:
    button_c = st.button('C', key='but_c', type=st.session_state.get("type_c", "secondary"), on_click=disable_other_parent, args=("c",), disabled=st.session_state.get("disabled_c", False))
    st.write("---")
    button_07 = st.button('07', key='but_07', type=st.session_state.get("type_07", "secondary"), on_click=disable_other_child, args=("07",), disabled=st.session_state.get("disabled_07", False))
    button_08 = st.button('08', key='but_08', type=st.session_state.get("type_08", "secondary"), on_click=disable_other_child, args=("08",), disabled=st.session_state.get("disabled_08", False))
    button_09 = st.button('09', key='but_09', type=st.session_state.get("type_09", "secondary"), on_click=disable_other_child, args=("09",), disabled=st.session_state.get("disabled_09", False))
    
with col16:
    button_d = st.button('D', key='but_d', type=st.session_state.get("type_d", "secondary"), on_click=disable_other_parent, args=("d",), disabled=st.session_state.get("disabled_d", False))
    st.write("---")
    button_10 = st.button('10', key='but_10', type=st.session_state.get("type_10", "secondary"), on_click=disable_other_child, args=("10",), disabled=st.session_state.get("disabled_10", False))
    button_11 = st.button('11', key='but_11', type=st.session_state.get("type_11", "secondary"), on_click=disable_other_child, args=("11",), disabled=st.session_state.get("disabled_11", False))
    button_12 = st.button('12', key='but_12', type=st.session_state.get("type_12", "secondary"), on_click=disable_other_child, args=("12",), disabled=st.session_state.get("disabled_12", False))
    
with col17:
    button_e = st.button('E', key='but_e', type=st.session_state.get("type_e", "secondary"), on_click=disable_other_parent, args=("e",), disabled=st.session_state.get("disabled_e", False))
    st.write("---")
    button_13 = st.button('13', key='but_13', type=st.session_state.get("type_13", "secondary"), on_click=disable_other_child, args=("13",), disabled=st.session_state.get("disabled_13", False))
    button_14 = st.button('14', key='but_14', type=st.session_state.get("type_14", "secondary"), on_click=disable_other_child, args=("14",), disabled=st.session_state.get("disabled_14", False))
    button_15 = st.button('15', key='but_15', type=st.session_state.get("type_15", "secondary"), on_click=disable_other_child, args=("15",), disabled=st.session_state.get("disabled_15", False))

st.write("")
st.write(f"##### 所選儲格本週庫存變化")
col20, col21 = st.columns([9,1])

def reload_number_in_lot():
    number_in_lot = []
    for i in range(7):
        number_in_lot.append(random.randrange(1000, 10000))

    with col20:
        option = {
            "xAxis": {
                "type": "category",
                "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            },
            "yAxis": {"type": "value"},
            "series": [{"data": number_in_lot, "type": "line"}],
        }
        st_echarts(
            options=option, height="400px",
        )