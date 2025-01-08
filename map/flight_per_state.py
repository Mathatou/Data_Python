import folium
import pandas as pd
import geopandas as geopd

# Load data
airport_df = pd.read_csv("./csv/airports.csv", encoding='latin1')
flight_df = pd.read_csv("./csv/flights.csv", encoding='latin1')
states_df = pd.read_csv("./csv/states.csv", encoding='latin1')

# Ensure necessary columns are present
if not {'OriginState', 'OriginState'}.issubset(flight_df.columns):
    raise ValueError("The flights CSV must contain 'state' and 'origin' columns.")

if not {'name', 'latitude', 'longitude'}.issubset(states_df.columns):
    raise ValueError("The states CSV must contain 'name', 'latitude', and 'longitude' columns.")

# Aggregate number of flights per state
flights_per_state = flight_df.groupby('OriginState').size().reset_index(name='num_flights')

# Load GeoJSON data
usa_states = geopd.read_file("./map/geous.geojson")

# Merge GeoJSON data with flight data
usa_states = usa_states.merge(
                              flights_per_state, 
                              left_on="name", 
                              right_on="OriginState", 
                              how="left"
                            )


# pandas 3.0 future warning the line 29 won't work with future versions of pandas
# the error message suggested line 30 to replace it
#usa_states["num_flights"].fillna(0, inplace=True) 
usa_states.fillna({"num_flights":0}, inplace=True)

# Create map centered on Washington DC
Washington_DC_coordinate = (38.889805, -77.009056)
us_map = folium.Map(location=Washington_DC_coordinate, tiles='OpenStreetMap', zoom_start=4)

# Add choropleth layer
folium.Choropleth(
    geo_data=usa_states,
    name="choropleth",
    #data=flights_per_state,
    data=usa_states[usa_states["num_flights"] >= 0],  # Exclude no-data states
    columns=["OriginState", "num_flights"],
    key_on="feature.properties.name",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Number of Flights per State",
).add_to(us_map)

# Layer for data states
for _, row in usa_states[usa_states["num_flights"] >= 0].iterrows():
    folium.GeoJson(
        row["geometry"],
        style_function=lambda x: {"fillColor": "blue", "color": "black", "weight": 0, "fillOpacity": 0},
        tooltip = f"For {row['name']}, {[row['fullname']]}, there are {[row['num_flights']]} flights between 2015 and 2020"
    ).add_to(us_map)


# Layer for no-data states
for _, row in usa_states[usa_states["num_flights"] <= 0].iterrows():
    folium.GeoJson(
        row["geometry"],
        style_function=lambda x: {"fillColor": "orange", "color": "grey", "weight": 0.5, "fillOpacity": 0.7},
        tooltip=f"For {row['name']}, Maryland : No Data",
    ).add_to(us_map)

# Save the map
us_map.save(outfile='flight_per_state.html')
