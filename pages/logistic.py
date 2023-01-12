import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

with st.sidebar.form(key="my_form"):
    selectbox_state = st.selectbox("請輸入您想查詢的貨物編號", ['BNA05201624', 'BNA17160650', 'BNA28408227', 'PNA07065293', 'PNA13696387', 'PNA24590925', 'GRP07979783', 'GRP13478514', 'GRP27732412'])
    pressed = st.form_submit_button("確認")
st.header("出貨狀況")
def show_table(number):
    df = pd.DataFrame(np.array([[number, '2023/1/11 10:34:45', '運送中']]), columns=(['貨物編號', '出貨時間', '貨物狀態']))
    st.table(df)

if pressed:
    show_table(number = selectbox_state)

df = pd.read_json('route3.json')
st.header("貨物位置")
st.dataframe(df)

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

df['顏色'] = df['顏色'].apply(hex_to_rgb)
view_state = pdk.ViewState(
    latitude=23.5,
    longitude=120.8984867,
    zoom=6
)

layer = pdk.Layer(
    type='PathLayer',
    data=df,
    pickable=True,
    get_color='顏色',
    width_scale=20,
    width_min_pixels=2,
    get_path='路徑',
    get_width=5
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"style":{"color":"white"}})

st.pydeck_chart(r)