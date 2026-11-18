import streamlit as st
import geopandas as gpd
import shapely
import pandas as pd
from streamlit_folium import st_folium  

from shapely.geometry import Point, Polygon

st.set_page_config(
    page_title="Laboratorium GIS",
    layout="wide"
)


#------------------------------------------------------------------------------
st.header("A1. Geometria i GeoDataFrame od zera")

# Tworzenie punktu - Rynek w Opolu
rynek = Point(17.9226, 50.6681)

square = Polygon([
    (17.92, 50.66),
    (17.93, 50.66),
    (17.93, 50.67),
    (17.92, 50.67)
])


st.write("Lokalizacja Rynku:", rynek)
st.write("Utworzony wielokąt:", square)
st.write("Pole wielokąta:", square.area)
st.write("Czy Rynek znajduje się w wielokącie?", square.contains(rynek))

places = gpd.GeoDataFrame(
    {"name": ["Rynek", "Square"]},
    geometry=[rynek, square],
    crs="EPSG:4326"
)

st.write("tabela przestrzenna:")

places_display = places.copy()
places_display["geometry"] = places_display.geometry.to_wkt()
st.dataframe(places_display, use_container_width=True)


st.write("Typ obiektu:", type(places))
st.write("Układ współrzędnych:", places.crs)
st.write("Typy geometrii:", places.geom_type.tolist())

#------------------------------------------------------------------------------
st.header("A2. Wczytanie surowych danych")

raw = pd.read_csv("dane/pm25_sensors.csv", parse_dates=["measured_at"])
st.write("Rozmiar:", raw.shape)
st.write("Pierwsze 10 wierszy:", raw.head(10))


st.write("Opis danych:", raw[["lat", "lon", "pm25"]].describe())
st.write("NA:", raw.isna().sum())
st.write("Dublikaty:", raw.duplicated().sum())

#------------------------------------------------------------------------------
st.header("A3. Czyszczenie danych")

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

st.write("Raport czyszczenia danych: ", report)
st.write("Opis danych po czyszczeniu: ", df[["lat", "lon", "pm25"]].describe())

#------------------------------------------------------------------------------
st.header("A4. Z tabeli do GeoDataFrame")

sensors = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["lon"], df["lat"]),   # x = lon, y = lat!
    crs="EPSG:4326",
)
st.write("Pierwsze 5 wierszy:", sensors.head())
st.write("Typy geometrii:", sensors.geom_type.unique())
st.write("Układ współrzędnych:", sensors.crs)
st.write("Granice danych:", sensors.total_bounds)              # [minx, miny, maxx, maxy]

st.header("4. Mapa czujników PM2.5")

sensor_map = sensors.explore(
    column="pm25",
    cmap="Oranges",
    marker_kwds={"radius": 6},
    tooltip=["pm25"]
)

st_folium(
    sensor_map,
    width=None,
    height=600
)
#------------------------------------------------------------------------------
st.header("5. Eksperyment – zamiana współrzędnych")

sensors_wrong = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(
        df["lat"],  # BŁĘDNIE: latitude jako X
        df["lon"]   # BŁĘDNIE: longitude jako Y
    ),
    crs="EPSG:4326"
)

st.subheader("Mapa po zamianie współrzędnych")

wrong_map = sensors_wrong.explore(
    column="pm25",
    cmap="Oranges",
    marker_kwds={"radius": 6},
    tooltip=["pm25"]
)

st_folium(
    wrong_map,
    width=None,
    height=600
)