import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from dash.dependencies import Input, Output

class FlightDistanceDistribution:
    def __init__(self, app, flights_df):
        """Initializes the FlightDistanceDistribution"""
        self.app = app
        self.flights_df = flights_df
        self.component_id = 'flight-distance-distribution'
        self._register_callbacks()

    def create_component(self):
        """Creates the component layout"""
        return html.Div([
            dcc.Dropdown(
                id=f'{self.component_id}-chart-type',
                options=[
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Histogram', 'value': 'histogram'}
                ],
                value='histogram',  
                clearable=False,
                className='mb-3'
            ),
            html.Div(
                id=f'{self.component_id}-bin-size-container',
                children=[
                    dcc.Dropdown(
                        id=f'{self.component_id}-distance-bin-size',
                        options=[
                            {'label': '100 miles', 'value': 100},
                            {'label': '250 miles', 'value': 250},
                            {'label': '500 miles', 'value': 500},
                            {'label': '1000 miles', 'value': 1000}
                        ],
                        value=500, 
                        clearable=False,
                        className='mb-3'
                    )
                ]
            ),
            dcc.Graph(id=f'{self.component_id}-graph')
        ])

    def _register_callbacks(self):
        """Registers callbacks"""
        @self.app.callback(
            Output(f'{self.component_id}-bin-size-container', 'style'),
            [Input(f'{self.component_id}-chart-type', 'value')]
        )
        def toggle_bin_size_dropdown(chart_type):
            """Hides the bin size dropdown when in histogram mode"""
            return {'display': 'block' if chart_type == 'bar' else 'none'}

        @self.app.callback(
            Output(f'{self.component_id}-graph', 'figure'),
            [Input(f'{self.component_id}-chart-type', 'value'),
             Input(f'{self.component_id}-distance-bin-size', 'value')]
        )
        def update_graph(chart_type, distance_bin_size):
            if chart_type == 'bar':
                return self._create_bar_chart(distance_bin_size)
            elif chart_type == 'histogram':
                return self._create_histogram()

    def _create_bar_chart(self, distance_bin_size):
        """Creates a bar chart showing the number of flights by distance range"""
        max_distance = self.flights_df['Distance'].max()
        bins = list(range(0, int(max_distance) + distance_bin_size, distance_bin_size))
        labels = [f"{bins[i]}-{bins[i+1]} miles" for i in range(len(bins) - 1)]

        self.flights_df['DistanceRange'] = pd.cut(
            self.flights_df['Distance'],
            bins=bins,
            labels=labels,
            right=False
        )

        flights_per_distance = self.flights_df['DistanceRange'].value_counts().sort_index().reset_index()
        flights_per_distance.columns = ['DistanceRange', 'NumFlights']

        bar_chart = go.Figure()

        bar_chart.add_trace(go.Bar(
            x=flights_per_distance['DistanceRange'],
            y=flights_per_distance['NumFlights'],
            name='Number of Flights',
            marker_color='#1f77b4',  
            hovertemplate="<b>%{x}</b><br>Number of Flights: %{y:,}<extra></extra>"
        ))

        bar_chart.update_layout(
            title=dict(
                text='Number of Flights by Flight Distance (Bar Chart)',
                font=dict(size=24),
                y=0.95
            ),
            xaxis=dict(
                title=dict(
                    text="Flight Distance Range (miles)",
                    font=dict(size=16)
                ),
                tickangle=45,
                showgrid=False
            ),
            yaxis=dict(
                title=dict(
                    text="Number of Flights",
                    font=dict(size=16)
                ),
                showgrid=True,
                gridcolor='rgba(211, 211, 211, 0.5)'
            ),
            plot_bgcolor='white',
            hoverlabel=dict(bgcolor="white"),
            margin=dict(t=100, l=80, r=40, b=120),
        )

        return bar_chart

    def _create_histogram(self):
        """Creates a histogram showing the number of flights by distance (1-mile steps)"""
        histogram = go.Figure()

        histogram.add_trace(go.Histogram(
            x=self.flights_df['Distance'],
            name='Number of Flights',
            marker_color='#1f77b4',  
            hovertemplate="<b>%{x} miles</b><br>Number of Flights: %{y:,}<extra></extra>",
            xbins=dict(
                start=0,
                end=self.flights_df['Distance'].max(),
                size=1
            )
        ))

        histogram.update_layout(
            title=dict(
                text='Number of Flights by Flight Distance (Histogram)',
                font=dict(size=24),
                y=0.95
            ),
            xaxis=dict(
                title=dict(
                    text="Flight Distance (miles)",
                    font=dict(size=16)
                ),
                showgrid=False
            ),
            yaxis=dict(
                title=dict(
                    text="Number of Flights",
                    font=dict(size=16)
                ),
                showgrid=True,
                gridcolor='rgba(211, 211, 211, 0.5)'
            ),
            plot_bgcolor='white',
            hoverlabel=dict(bgcolor="white"),
            margin=dict(t=100, l=80, r=40, b=120),
            height=700
        )

        return histogram