import streamlit as st
import pandas as pd
import pydeck as pdk
import json

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

# Dynamic view state
view_state = pdk.ViewState(
    latitude=filtered_df['latitude'].mean(),
    longitude=filtered_df['longitude'].mean(),
    zoom=12,
    pitch=50
)

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(filtered_df))
col2.metric("Avg Stress Score", f"{filtered_df['Stress_Score'].mean():.2f}")
col3.metric("Max Traffic Volume", int(filtered_df['Traffic Volume'].max()))

with open("data/bengaluru_boundary.geojson") as f:
    gj_data = json.load(f)

# Create the Boundary Layer
boundary_layer = pdk.Layer(
    "GeoJsonLayer",
    gj_data,
    opacity=0.1,
    stroked=True,
    filled=True,
    get_line_color=[255, 255, 255], # White border
    get_fill_color=[200, 200, 200, 50], # Faint grey fill
    line_width_min_pixels=2,
)

hexa_layer = pdk.Layer(
    "HexagonLayer",
    data=filtered_df,
    get_position='[longitude, latitude]',
    radius=250,
    elevation_scale=50,
    elevation_range=[0, 1000],
    get_fill_color="[255 * (Stress_Score/100), 255 * (1 - Stress_Score/100), 0, 160]", 
    pickable=True,
    extruded=True,
)

# The 3D Hexagon Map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=pdk.ViewState(latitude=12.9716, longitude=77.5946, zoom=11, pitch=45),
    layers=[boundary_layer,hexa_layer]
))