from dash import html
import dash_bootstrap_components as dbc
from src.components.plot.time_distribution_component import TimeDistributionComponent
import pandas as pd

def create_layout(app, flights_df):
    time_distribution = TimeDistributionComponent(app, flights_df)

    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Temporal Models", className="text-center mb-4"))
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Flights Distribution by Time Period"),
                    dbc.CardBody(time_distribution.create_component())
                ], className="mb-4 shadow")
            ], width=12, lg=12),
        ]),        
    ], fluid=True)
