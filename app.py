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

    df = df.rename(columns={
        "lat": "latitude",
        "lon": "longitude",
        "long": "longitude",
        "station": "station_name",
        "name": "station_name",
        "districts": "district",
        "type": "station_type"
    })

    return df


# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Suriname Station Metadata Map",
    layout="wide"
)

st.title("Suriname Station Metadata Map")
st.write("Interactieve kaart met metadata van meteorologische stations in Suriname.")


# -----------------------------
# Load Data
# -----------------------------
df = load_metadata()


# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

# District filter
if "district" in df.columns:
    district_list = ["Alle"] + sorted(df["district"].dropna().unique().tolist())
    selected_district = st.sidebar.selectbox("District", district_list)
else:
    selected_district = "Alle"

# Station type filter
if "station_type" in df.columns:
    type_list = ["Alle"] + sorted(df["station_type"].dropna().unique().tolist())
    selected_type = st.sidebar.selectbox("Station Type", type_list)
else:
    selected_type = "Alle"

# Filter logic
filtered_df = df.copy()

if selected_district != "Alle":
    filtered_df = filtered_df[filtered_df["district"] == selected_district]

if selected_type != "Alle":
    filtered_df = filtered_df[filtered_df["station_type"] == selected_type]


# -----------------------------
# Map Center
# -----------------------------
if len(filtered_df) > 0:
    center_lat = filtered_df["latitude"].mean()
    center_lon = filtered_df["longitude"].mean()
else:
    center_lat, center_lon = 5.8, -55.2


# -----------------------------
# Folium Map
# -----------------------------
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

for _, row in filtered_df.iterrows():

    popup_html = f"""
    <div style='font-size:14px; line-height:1.4'>
        <b style='font-size:16px'>{row.get('station_name', 'Onbekend')}</b><br><br>
        <b>WIGOS:</b> {row.get('wigos_id', 'n/a')}<br>
        <b>District:</b> {row.get('district', 'n/a')}<br>
        <b>Type:</b> {row.get('station_type', 'n/a')}<br>
        <b>Elevation:</b> {row.get('elevation', 'n/a')} m<br>
        <b>Instruments:</b> {row.get('instruments', 'n/a')}<br>
        <b>Frequency:</b> {row.get('frequency', 'n/a')}
    </div>
    """

    folium.Marker(
        [row["latitude"], row["longitude"]],
        popup=popup_html,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)


# -----------------------------
# Display Map
# -----------------------------
st_folium(m, width=900, height=550)
