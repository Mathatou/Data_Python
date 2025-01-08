import folium
import pandas as pd
import geopandas as geopd

airport_df = pd.read_csv("./csv/airports.csv", encoding='latin1')
flight_df = pd.read_csv("./csv/flights.csv", encoding='latin1')
states_df = pd.read_csv("./csv/states.csv", encoding='latin1')

Washington_DC_coordinate = (38.889805, -77.009056)

# Vérifiez que les colonnes nécessaires sont présentes
if not {'latitude_deg', 'longitude_deg', 'name'}.issubset(airport_df.columns):
    raise ValueError("Le fichier CSV doit contenir les colonnes 'latitude_deg', 'longitude_deg', et 'name'.")
# Crer une map centrée sur Washington DC
us_map = folium.Map(location=Washington_DC_coordinate, tiles='OpenStreetMap', zoom_start=4)

# Cercle sur chaque états
radius = 10
for _, row in states_df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius= radius,
        color="cornflowerblue",
        stroke=False,
        fill=True,
        fill_opacity=0.6,
        opacity=1,
        popup="{} pixels".format(radius),
        tooltip=row["name"],   
    ).add_to(us_map)

## CHLOROPLETH
usa_states = geopd.read_file("map/geous.geojson")

folium.Choropleth(

    geo_data=usa_states,

    data=airport_df,

    columns=["type", "id"],

    key_on="feature.properties.name",

).add_to(us_map)


us_map.save(outfile='map.html')
