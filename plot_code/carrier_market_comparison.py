import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from dash.dependencies import Input, Output
import geopandas as gpd
import folium

class CarrierMarketComparisonComponent:
    def __init__(self, app, df, states_geojson_path):
        """Initializes the CarrierMarketComparisonComponent"""
        self.app = app
        self.df = df
        self.states_geojson_path = states_geojson_path
        self.component_id = 'carrier-comparison'
        self._register_callbacks()

    def create_component(self):
        """Creates the component layout"""
        return html.Div([
            dcc.Dropdown(
                id=f'{self.component_id}-chart-type',
                options=[
                    {'label': 'Pie Chart', 'value': 'pie'},
                    {'label': 'Map', 'value': 'map'}
                ],
                value='map',
                clearable=False,
                className='mb-3'
            ),
            html.Div(id=f'{self.component_id}-graph-container')
        ])

    def _register_callbacks(self):
        """Registers callbacks"""
        @self.app.callback(
            Output(f'{self.component_id}-graph-container', 'children'),
            [Input(f'{self.component_id}-chart-type', 'value')]
        )
        def update_graph(chart_type):
            if chart_type == 'pie':
                return dcc.Graph(figure=self._create_pie_chart())
            elif chart_type == 'map':
                return self._create_map()

    def _create_pie_chart(self):
        """Creates a pie chart to compare the number of flights by carrier"""
        flights_per_carrier = self.df.groupby('Reporting_Airline').size().reset_index(name='num_flights')

        colors = [
            '#1f77b4',  
            '#ff7f0e',  
            '#2ca02c',  
            '#d62728',  
            '#9467bd',  
            '#8c564b',  
            '#e377c2',  
            '#7f7f7f',  
            '#bcbd22',  
            '#17becf'   
        ]

        pie_chart = go.Figure()

        pie_chart.add_trace(go.Pie(
            labels=flights_per_carrier['Reporting_Airline'],
            values=flights_per_carrier['num_flights'],
            name='Flights',
            hovertemplate="<b>%{label}</b><br>Number of Flights: %{value:,.0f}<br>Percentage: %{percent}<extra></extra>",
            textinfo='percent+label',
            hole=0.4,
            marker=dict(colors=colors)
        ))

        pie_chart.update_layout(
            title=dict(
                text='Flight Distribution by Carrier',
                font=dict(size=24),
                y=0.95
            ),
            plot_bgcolor='white',
            hoverlabel=dict(bgcolor="white"),
            margin=dict(t=100, l=80, r=80, b=80),
            height=700,
            showlegend=False
        )

        return pie_chart

    def _create_map(self):
        """Creates a map showing the dominant carrier for each state using Folium"""
        states_df = pd.read_csv("csv/states.csv")
        state_abbr = dict(zip(states_df['name'], states_df['state']))

        self.df['OriginState'] = self.df['OriginState'].replace(state_abbr)

        usa_states = gpd.read_file(self.states_geojson_path)

        flights_per_state_carrier = self.df.groupby(['OriginState', 'Reporting_Airline']).size().reset_index(name='num_flights')

        dominant_carriers = flights_per_state_carrier.loc[
            flights_per_state_carrier.groupby('OriginState')['num_flights'].idxmax()
        ]

        airlines_df = pd.read_csv("csv/airlines.csv")
        carrier_name_map = dict(zip(airlines_df['Carrier'], airlines_df['CarrierName']))
        dominant_carriers['CarrierName'] = dominant_carriers['Reporting_Airline'].map(carrier_name_map)

        usa_states = usa_states.merge(
            dominant_carriers,
            left_on="name",
            right_on="OriginState",
            how="left"
        )

        us_map = folium.Map(location=[37.0902, -95.7129], tiles='OpenStreetMap', zoom_start=4)

        title_html = """
            <h3 style='font-size: 1.5em;'>
                Dominant Carrier by State
            </h3>
        """
        us_map.get_root().html.add_child(folium.Element(title_html))

        folium.GeoJson(
            usa_states,
            style_function=lambda feature: {
                "fillColor": "white",
                "color": "black",
                "weight": 0.5,
                "fillOpacity": 0.7,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['name', 'CarrierName', 'num_flights'],
                aliases=['State:', 'Dominant Carrier:', 'Number of Flights:'],
                localize=True,
                sticky=True,
                labels=True,
                style="""
                    background-color: white;
                    font-size: 16px;
                    padding: 5px;
                """
            ),
            popup=folium.GeoJsonPopup(
                fields=['name', 'CarrierName', 'num_flights'],
                aliases=['State:', 'Dominant Carrier:', 'Number of Flights:'],
                localize=True,
                labels=True,
                style="""
                    background-color: white;
                    font-size: 16px;
                    padding: 5px;
                """
            )
        ).add_to(us_map)

        carrier_names_group = folium.FeatureGroup(name="Carrier Names", show=True)

        for _, row in usa_states.iterrows():
            if pd.notna(row['CarrierName']):
                centroid = row['geometry'].centroid
                folium.Marker(
                    location=[centroid.y, centroid.x],
                    icon=folium.DivIcon(
                        html=f"""
                            <div style='
                                font-size: 10px;
                                font-weight: bold;
                                text-align: center;
                                line-height: 1.5;
                                width: 100%;
                                height: 100%;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                            '>
                                {row['CarrierName']}
                            </div>
                        """
                    )
                ).add_to(carrier_names_group)

        carrier_names_group.add_to(us_map)

        folium.LayerControl().add_to(us_map)

        map_html = us_map.get_root().render()
        return html.Iframe(
            srcDoc=map_html,
            style={'width': '100%', 'height': '650px'}
        )