import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

def load_metadata():
    df = pd.read_excel("data/stations_metadata.xlsx")
    df.columns = df.columns.str.lower()

    df = df.rename(columns={
        "lat": "latitude",
        "lon": "longitude",
        "long": "longitude"
    })

    return df

df = load_metadata()

st.title("Suriname Station Metadata Map")

m = folium.Map(location=[5.8, -55.2], zoom_start=7)

for _, row in df.iterrows():
    popup = f"""
    <b>{row['station_name']}</b><br>
    WIGOS: {row['wigos_id']}<br>
    Elevation: {row['elevation']} m<br>
    Instruments: {row['instruments']}<br>
    Frequency: {row['frequency']}
    """
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=popup
    ).add_to(m)

st_folium(m, width=700, height=500)

