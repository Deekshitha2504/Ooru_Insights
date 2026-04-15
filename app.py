import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_icon="💛❤️", page_title="Ooru_insights", layout="wide", initial_sidebar_state="collapsed")

# Load the data from the data folder
@st.cache_data
def load_data():
    return pd.read_csv("data/Banglore_traffic_Cleaned.csv")

df = load_data()

st.title("🚦 Ooru_insights: Traffic Stress Map")

# Sidebar for Filtering
area = st.sidebar.multiselect("Select Area", options=df['Area Name'].unique(), default=df['Area Name'].unique()[:5])
filtered_df = df[df['Area Name'].isin(area)]

# The 3D Hexagon Map
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(latitude=12.9716, longitude=77.5946, zoom=11, pitch=45),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=filtered_df,
            get_position='[longitude, latitude]',
            radius=200,
            elevation_scale=10, # Height of the towers
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))