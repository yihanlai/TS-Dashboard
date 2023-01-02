import streamlit as st

import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

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

def generate_random_ratio(num):
    list1 = np.random.randint(10, 100, size=num)
    ratio = 100/ sum(list1)
    return list1 / ratio

storage_records = {'siteA': generate_random_ratio(3),
                   'siteB': generate_random_ratio(3),
                   'siteC': generate_random_ratio(3),
                   }
inventory_records = {'siteA': generate_random_ratio(4),
                     'siteB': generate_random_ratio(4),
                     'siteC': generate_random_ratio(4),
                    }



st.set_page_config(layout="wide", page_title="dashboard app")
st.title('倉儲 Dashboard')

# selet sites
all_sites = ['siteA', 'siteB', 'siteC']
sites = st.multiselect("Choose sites to visualize", all_sites, all_sites[:2])


col11, col12 = st.columns(2)
col11.markdown('#### Temperature')
temp_data = {
        'site': ['siteA']*31 + ['siteB']*31 + ['siteC']*31,
        'date': np.tile(pd.date_range('2022-12-01','2022-12-31'), 3), 
        'temperature': np.round(np.random.uniform(15,25,31*3), 1),
        }
temp_df = pd.DataFrame(temp_data)

temp_df = temp_df[temp_df.site.isin(sites)]
chart = get_line_chart(temp_df, "date", "temperature", "12月每日平均溫度")
col11.altair_chart(chart, use_container_width=True)


col12.markdown('#### Humidity')
humid_data = {
    'site': ['siteA']*31 + ['siteB']*31 + ['siteC']*31,
    'date': np.tile(pd.date_range('2022-12-01','2022-12-31'), 3), 
    'humidity': np.round(np.random.uniform(15,40,31*3), 1),
    }
humid_df = pd.DataFrame(humid_data)

humid_df = humid_df[humid_df.site.isin(sites)]
chart = get_line_chart(humid_df, "date", "humidity", "12月每日平均濕度")
col12.altair_chart(chart, use_container_width=True)


for site in sites:
    st.write(f"####  Information of {site}")
    col21, col22, col23 = st.columns(3)
    color = plt.cm.get_cmap('tab20c')
    
    col21.markdown('#### Storage Utilization')
    col21.markdown('###### 倉庫使用率')
    labels = ['Empty', 'Reserved', 'Occupied']
    sizes = storage_records[site]
    colors = color(np.array([1,2,3]))
    fig1 = get_pie_chart(sizes, labels, colors)
    col21.pyplot(fig1)

    col22.markdown('#### Inventory Type')
    col22.markdown('###### 庫存類型比例')
    labels = ['Finished\nProducts', 'Semi-Finished\nProducts', 'Defective\nProducts', 'Raw\nMaterial']
    sizes = inventory_records[site]
    colors = color(np.array([5,6,7,8]))
    fig2 = get_pie_chart(sizes, labels, colors)
    col22.pyplot(fig2)



