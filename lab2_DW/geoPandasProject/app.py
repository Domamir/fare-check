import streamlit as st
import geopandas as gpd
import rasterio
import shapely
from shapely.geometry import Point, Polygon
import pandas as pd
import streamlit.components.v1 as components

st.title("Lab 2 – GeoPandas")

rynek = Point(17.9226, 50.6681)          # (x, y) = (longitude, latitude)
square = Polygon([(17.92, 50.66), (17.93, 50.66), (17.93, 50.67), (17.92, 50.67)])

places = gpd.GeoDataFrame(
    {"name": ["Rynek", "Square"]},
    geometry=[rynek, square],
    crs="EPSG:4326",                     # WGS 84 - longitude/latitude in degrees
)

raw = pd.read_csv("dane/pm25_sensors.csv", parse_dates=["measured_at"])
st.write("Rozmiar danych:", raw.shape)

st.subheader("Pierwsze 10 wierszy")
st.dataframe(raw.head(10))

st.subheader("Statystyki opisowe")
st.dataframe(raw[["lat", "lon", "pm25"]].describe())

st.subheader("Braki danych")
st.dataframe(raw.isna().sum())

st.subheader("Duplikaty")
st.write("Liczba zduplikowanych wierszy:", raw.duplicated().sum())

# Czyszczenie danych

df = raw.copy()
report = {"input rows": len(df)}

# 1. Duplicates - the same message sent twice
df = df.drop_duplicates()
report["after drop_duplicates"] = len(df)

# 2. Rows without coordinates cannot be placed on a map
df = df.dropna(subset=["lat", "lon"])
report["after dropna"] = len(df)

# 3. Swapped coordinates: in Poland lat is 49-55 and lon is 14-24
swapped = df["lat"].between(14, 24.5) & df["lon"].between(49, 55)
df.loc[swapped, ["lat", "lon"]] = df.loc[swapped, ["lon", "lat"]].to_numpy()
report["swapped rows fixed"] = int(swapped.sum())

# 4. -999 is the sensor's error code, not a measurement
df = df[df["pm25"] >= 0].reset_index(drop=True)
report["clean rows"] = len(df)

st.subheader("Dane po czyszczeniu")
st.write(report)

st.subheader("Statystyki opisowe po czyszczeniu")
st.dataframe(df[["lat", "lon", "pm25"]].describe())

df[["lat", "lon", "pm25"]].describe().round(2)

# Wizualizacja

sensors = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["lon"], df["lat"]),   # x = lon, y = lat!
    crs="EPSG:4326",
)

st.subheader("Sensors")
st.write(sensors.head())

st.subheader("Typ geometryczny")
st.write(sensors.geom_type.unique())

st.subheader("CRS")
st.write(sensors.crs)

st.subheader("Total bounds")
st.write(sensors.total_bounds)         # [minx, miny, maxx, maxy]

st.subheader("Interaktywna mapa")
m = sensors.explore(column="pm25", cmap="Oranges", marker_kwds={"radius": 6})
components.html(m.get_root().render(), height=500)