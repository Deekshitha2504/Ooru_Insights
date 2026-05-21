import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import json

st.set_page_config(page_title="Ooru_insights", layout="wide")

st.title("🚦 Ooru_insights: Bengaluru Traffic Command Center")
st.markdown("---")

@st.cache_data
def load_data():
    data = pd.read_csv("data/Banglore_traffic_Cleaned.csv")
    
    if 'Hour' not in data.columns and 'Timestamp' in data.columns:
        data['Hour'] = pd.to_datetime(data['Timestamp']).dt.hour
    elif 'Hour' not in data.columns:
        data['Hour'] = 12 
        
    return data

df = load_data()

left_col, mid_col, right_col = st.columns([1, 2, 0.8])

with left_col:
    st.subheader("📊 Traffic Trends")

    top_areas = df.groupby('Area Name')['Traffic Volume'].mean().sort_values(ascending=False).head(5).reset_index()
    fig1 = px.bar(
        top_areas, 
        x='Traffic Volume', 
        y='Area Name', 
        orientation='h', 
        title="Top 5 Congested Areas",
        color_discrete_sequence=['#FF4B4B']
    )
    fig1.update_layout(height=280, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("~~~~~~~~")

    extra_insight = st.selectbox(
        "Select Detailed Insight:",
        ["Stress by Hour", "Environmental Impact"]
    )

    if extra_insight == "Stress by Hour":
        hour_data = df.groupby('Hour')['Stress_Score'].mean().reset_index()
        fig2 = px.line(
            hour_data, 
            x='Hour', 
            y='Stress_Score', 
            title="Stress Over Time",
            color_discrete_sequence=['#00CC96']
        )
        fig2.update_layout(height=280, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig2, use_container_width=True)
        
    elif extra_insight == "Environmental Impact":
        impact_data = df.groupby('Area Name')['Environmental Impact'].mean().sort_values(ascending=False).head(5).reset_index()
        fig2 = px.bar(
            impact_data, 
            x='Area Name', 
            y='Environmental Impact', 
            title="Highest Environmental Impact Areas",
            color_discrete_sequence=['#AB63FA']
        )
        fig2.update_layout(height=280, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig2, use_container_width=True)


with mid_col:
    st.subheader("🗺️ Spatial Traffic Heatmap")
    
    day_type = st.radio(
        "📅 Select Travel Period Profile:",
        options=["Weekday Patterns", "Weekend Patterns"]
    )
    
    weekend_flag = 1 if day_type == "Weekend Patterns" else 0

    map_df = df[df['Is_Weekend'] == weekend_flag]
    
    if map_df.empty:
        map_df = df

    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=map_df,
        get_position="[longitude, latitude]",
        get_weight="Stress_Score",
        radius_pixels=60,   
        intensity=1.8,      
        threshold=0.03,     
    )

    view_state = pdk.ViewState(
        latitude=12.9716,
        longitude=77.5946,
        zoom=10.8,
        pitch=0
    )

    st.pydeck_chart(pdk.Deck(
    map_style="dark", 
    map_provider="carto",
    initial_view_state=view_state,
    layers=[heatmap_layer]
))



with right_col:
    st.subheader("📈 City Metrics")
    st.info("Placeholder: Summary Metric cards will align here.")