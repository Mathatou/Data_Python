from dash import html
import dash_bootstrap_components as dbc
from src.components.plot.delay_distribution import DelayDistributionComponent
from src.components.plot.delay_duration import DelayDurationComponent
import pandas as pd


def create_layout(app, flights_df):
    delay_dist = DelayDistributionComponent(app, flights_df)
    delay_duration = DelayDurationComponent(flights_df)

    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Delay Analysis", className="text-center mb-4"))
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Flight Delays Distribution"),
                    dbc.CardBody(delay_dist.create_component())
                ], className="mb-4 shadow")
            ], width=12, lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Flight Delays Duration"),
                    dbc.CardBody(delay_duration.create_component())
                ], className="mb-4 shadow")
            ], width=12, lg=6),
        ]),
    ], fluid=True)
