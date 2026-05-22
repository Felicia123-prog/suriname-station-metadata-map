import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# -----------------------------
# Load metadata CSV
# -----------------------------
def load_metadata():
    df = pd.read_csv("data/MetaData_Meteo_Stations.csv")
    df.columns = df.columns.str.lower()

    # Kolomnamen normaliseren
    df = df.rename(columns={
        "lat": "latitude",
        "lon": "longitude",
        "long": "longitude",
        "station": "station_name",
        "name": "station_name"
    })

    return df


# -----------------------------
# Main App
# -----------------------------
st.set_page_config(page_title="Suriname Station Metadata Map", layout="wide")

st.title("Suriname Station Metadata Map")
st.write("Interactieve kaart met metadata van meteorologische stations in Suriname.")

df = load_metadata()

# -----------------------------
# Folium Map
# -----------------------------
m = folium.Map(location=[5.8, -55.2], zoom_start=7)

for _, row in df.iterrows():
    popup = f"""
    <b>{row.get('station_name', 'Onbekend')}</b><br>
    WIGOS: {row.get('wigos_id', 'n/a')}<br>
    Elevation: {row.get('elevation', 'n/a')} m<br>
    Instruments: {row.get('instruments', 'n/a')}<br>
    Frequency: {row.get('frequency', 'n/a')}
    """

    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=popup
    ).add_to(m)

st_folium(m, width=900, height=550)
