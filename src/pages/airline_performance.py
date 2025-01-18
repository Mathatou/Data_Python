from dash import html
import dash_bootstrap_components as dbc
from src.components.plot.airline_performance_comparison import AirlinePerformanceComponent
from src.components.plot.carrier_market_comparison import CarrierMarketComparisonComponent
import pandas as pd

def create_layout(app, flights_df, airlines_df, geojson_path):
    airline_performance = AirlinePerformanceComponent(app, flights_df, airlines_df)
    carrier_market = CarrierMarketComparisonComponent(app, flights_df, geojson_path)

    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Airline Performance", className="text-center mb-4"))
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Carrier Delays Comparison"),
                    dbc.CardBody(airline_performance.create_component())
                ], className="mb-4 shadow")
            ], width=12, lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Carrier Market Comparison"),
                    dbc.CardBody(carrier_market.create_component())
                ], className="mb-4 shadow")
            ], width=12, lg=6),
        ]),
    ], fluid=True)
