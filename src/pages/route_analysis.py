from dash import html
import dash_bootstrap_components as dbc
from src.components.plot.flight_distribution import FlightDistributionComponent
from src.components.plot.flight_distance_distribution import FlightDistanceDistribution
import pandas as pd

def create_layout(app, flights_df, states_df, geojson_path):
    flight_distribution = FlightDistributionComponent(app, flights_df, states_df, geojson_path)
    flight_distance = FlightDistanceDistribution(app, flights_df)

    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Route Analysis", className="text-center mb-4"))
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Flight Distribution Comparison"),
                    dbc.CardBody(flight_distribution.create_component())
                ], className="mb-4 shadow")
            ], width=12, lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Flight Distance Distribution"),
                    dbc.CardBody(flight_distance.create_component())
                ], className="mb-4 shadow")
            ], width=12, lg=6),
        ]),
    ], fluid=True)
