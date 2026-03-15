import streamlit as st
import pandas as pd

# 🎨 Branding (Keep that Karnataka Theme!)
st.set_page_config(page_title="LuruPulse", layout="wide")

# 📂 1. Load your local file (Replace 'your_data.csv' with your actual filename)
FILE_NAME = "Banglore_traffic_Dataset.csv" 

try:
    df = pd.read_csv(FILE_NAME)
    st.sidebar.success(f"✅ Loaded {FILE_NAME}")
except FileNotFoundError:
    st.sidebar.error(f"❌ Could not find {FILE_NAME}. Check the filename!")
    st.stop()

# 🏙️ 2. Title & Pulse
st.title("LuruPulse: Bengaluru Urban Analytics")
st.markdown("---")
age=st.button("click")
# 📊 3. The "Pulse" Dashboard (First look at your data)
st.subheader("Raw Data Preview")
st.dataframe(df.head(10)) # Shows the first 10 rows

# 🔍 4. Column Explorer (Let's see what we're working with)
st.columns.write("### Data Summary")
st.columns.write(f"Total Rows: {len(df)}")
st.columns.write(f"Columns: {list(df.columns)}")