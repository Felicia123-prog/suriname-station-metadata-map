import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ----------------------------------------------------
# Load metadata CSV
# ----------------------------------------------------
def load_metadata():
    df = pd.read_csv("data/MetaData_Meteo_Stations.csv")

    # Kolommen lowercase maken
    df.columns = df.columns.str.lower()

    # Kolommen mappen naar uniforme namen
    df = df.rename(columns={
        "station name": "station_name",
        "type": "station_type",
        "district": "district",
        "latitude": "latitude",
        "longitude": "longitude",
        "status": "status"
    })

    # Verwijder rijen zonder coordinaten
    df = df.dropna(subset=["latitude", "longitude"])

    return df


# ----------------------------------------------------
# Icon kleur per stationtype
# ----------------------------------------------------
def get_icon_color(station_type):
    if pd.isna(station_type):
        return "gray"

    station_type = station_type.lower()

    if "aws" in station_type:
        return "blue"
    if "synop" in station_type:
        return "red"
    if "ars" in station_type:
        return "green"

    return "gray"


# ----------------------------------------------------
# Streamlit Page Config
# ----------------------------------------------------
st.set_page_config(
    page_title="Suriname Station Metadata Map",
    layout="wide"
)

st.title("Suriname Station Metadata Map")
st.write("Interactieve kaart met metadata van meteorologische stations in Suriname.")

df = load_metadata()


# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------
st.sidebar.header("Filters")

# District filter
district_list = ["Alle"] + sorted(df["district"].dropna().unique().tolist())
selected_district = st.sidebar.selectbox("District", district_list)

# Station type filter
type_list = ["Alle"] + sorted(df["station_type"].dropna().unique().tolist())
selected_type = st.sidebar.selectbox("Station Type", type_list)

# Status filter
status_list = ["Alle"] + sorted(df["status"].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Status", status_list)


# ----------------------------------------------------
# Filter logic
# ----------------------------------------------------
filtered_df = df.copy()

if selected_district != "Alle":
    filtered_df = filtered_df[filtered_df["district"] == selected_district]

if selected_type != "Alle":
    filtered_df = filtered_df[filtered_df["station_type"] == selected_type]

if selected_status != "Alle":
    filtered_df = filtered_df[filtered_df["status"] == selected_status]


# ----------------------------------------------------
# Map Center
# ----------------------------------------------------
if len(filtered_df) > 0:
    center_lat = filtered_df["latitude"].mean()
    center_lon = filtered_df["longitude"].mean()
else:
    center_lat, center_lon = 5.8, -55.2


# ----------------------------------------------------
# Folium Map
# ----------------------------------------------------
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

for _, row in filtered_df.iterrows():

    popup_html = f"""
    <div style='font-size:14px; line-height:1.4'>
        <b style='font-size:16px'>{row.get('station_name', 'Onbekend')}</b><br><br>
        <b>Type:</b> {row.get('station_type', 'n/a')}<br>
        <b>District:</b> {row.get('district', 'n/a')}<br>
        <b>Status:</b> {row.get('status', 'n/a')}<br>
        <b>Latitude:</b> {row.get('latitude', 'n/a')}<br>
        <b>Longitude:</b> {row.get('longitude', 'n/a')}<br>
        <b>Begin Date:</b> {row.get('begin date', 'n/a')}<br>
        <b>End Date:</b> {row.get('end date', 'n/a')}
    </div>
    """

    folium.Marker(
        [row["latitude"], row["longitude"]],
        popup=popup_html,
        icon=folium.Icon(color=get_icon_color(row.get("station_type")), icon="info-sign")
    ).add_to(m)


# ----------------------------------------------------
# Display Map
# ----------------------------------------------------
st_folium(m, width=900, height=550)
