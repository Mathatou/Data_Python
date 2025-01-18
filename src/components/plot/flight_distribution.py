import folium
import pandas as pd
import numpy as np
import geopandas as gpd
from dash import html, dcc
from dash.dependencies import Input, Output

class FlightDistributionComponent:
    def __init__(self, app, flights_df, states_df, geojson_path):
        """Initializes the FlightDistributionComponent"""
        self.app = app
        self.flights_df = flights_df
        self.states_df = states_df
        self.geojson_path = geojson_path
        self.component_id = 'flight-distribution'
        self._register_callbacks()

    def create_component(self):
        """Creates the component layout"""
        return html.Div([
            dcc.Dropdown(
                id=f'{self.component_id}-view-type',
                options=[
                    {'label': 'State', 'value': 'state'},
                    {'label': 'Airport', 'value': 'airport'}
                ],
                value='state',
                clearable=False,
                className='mb-3'
            ),
            html.Iframe(id=f'{self.component_id}-map', style={'width': '100%', 'height': '650px'})
        ])

    def _register_callbacks(self):
        """Registers callbacks"""
        @self.app.callback(
            Output(f'{self.component_id}-map', 'srcDoc'),
            [Input(f'{self.component_id}-view-type', 'value')]
        )
        def update_map(view_type):
            if view_type == 'state':
                return self._create_state_map()
            elif view_type == 'airport':
                return self._create_airport_map()

    def _create_state_map(self):
        """Creates a map showing the number of flights per state"""
        # Load GeoJSON data
        usa_states = gpd.read_file(self.geojson_path)

        flights_per_state = self.flights_df.groupby('OriginState').size().reset_index(name='num_flights')

        usa_states = usa_states.merge(
            flights_per_state,
            left_on="name",
            right_on="OriginState",
            how="left"
        )

        usa_states.fillna({"num_flights": 0}, inplace=True)

        usa_states['log_num_flights'] = np.log10(usa_states['num_flights'].replace(0, 1))

        # Create map centered on Washington DC
        washington_dc_coordinate = (38.889805, -77.009056)
        us_map = folium.Map(location=washington_dc_coordinate, tiles='OpenStreetMap', zoom_start=4)

        max_log_flights = usa_states['log_num_flights'].max()
        bins = list(np.linspace(0, max_log_flights, num=10))  

        folium.Choropleth(
            geo_data=usa_states,
            name="choropleth",
            data=usa_states[usa_states["num_flights"] >= 0],  
            columns=["OriginState", "log_num_flights"], 
            key_on="feature.properties.name",
            fill_color="YlGnBu",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Number of Flights per State",
            bins=bins, 
            reset=True
        ).add_to(us_map)

        for _, row in usa_states[usa_states["num_flights"] > 0].iterrows():
            folium.GeoJson(
                row["geometry"],
                style_function=lambda x: {"fillColor": "blue", "color": "black", "weight": 0, "fillOpacity": 0},
                tooltip=f"For {row['name']}, {row['fullname']}, there are {row['num_flights']} flights between 2015 and 2020"
            ).add_to(us_map)

        for _, row in usa_states[usa_states["num_flights"] <= 0].iterrows():
            folium.GeoJson(
                row["geometry"],
                style_function=lambda x: {"fillColor": "orange", "color": "grey", "weight": 0.5, "fillOpacity": 0.7},
                tooltip=f"For {row['name']}, {row['fullname']} : No Data",
            ).add_to(us_map)

        return us_map.get_root().render()

    def _create_airport_map(self):
        """Creates a map showing the number of flights per airport"""

        flights_per_airport = self.flights_df.groupby(['Origin', 'OriginCityName', 'OriginState']).size().reset_index(name='num_flights')

        flights_per_airport = flights_per_airport[flights_per_airport['num_flights'] > 500]

        airports_df = pd.read_csv("data/csv/airports.csv")  
        airports_df = airports_df[['iata_code', 'latitude_deg', 'longitude_deg']]  

        flights_per_airport = flights_per_airport.merge(
            airports_df,
            left_on='Origin',
            right_on='iata_code',
            how='left'
        )

        flights_per_airport.dropna(subset=['latitude_deg', 'longitude_deg'], inplace=True)

        # Create map centered on Washington DC
        washington_dc_coordinate = (38.889805, -77.009056)
        us_map = folium.Map(location=washington_dc_coordinate, tiles='OpenStreetMap', zoom_start=4)

        for _, row in flights_per_airport.iterrows():
            folium.Circle(
                location=(row['latitude_deg'], row['longitude_deg']),  
                radius=row['num_flights'] * 10,  
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                tooltip=f"{row['Origin']} ({row['OriginCityName']}, {row['OriginState']}): {row['num_flights']} flights"
            ).add_to(us_map)

        return us_map.get_root().render()