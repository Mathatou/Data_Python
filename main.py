from utils.extract_csv import extract_if_needed
import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from plot_code.delay_distribution import DelayDistributionComponent
from plot_code.time_distribution_component import TimeDistributionComponent 
from plot_code.delay_duration import DelayDurationComponent 
from plot_code.airline_performance_comparison import AirlinePerformanceComponent
from plot_code.carrier_market_comparison import CarrierMarketComparisonComponent
from plot_code.flight_distribution import FlightDistributionComponent


def main():
    extract_if_needed()
   
    flights_df = pd.read_csv("csv/flights.csv", encoding='latin1')
    states_df = pd.read_csv("csv/states.csv", encoding='latin1')
    geojson_path = "data/geojson/geous.geojson"

    airlines_df = pd.read_csv("./csv/airlines.csv", encoding='latin1')

    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    delay_dist = DelayDistributionComponent(app, flights_df)
    time_dist = TimeDistributionComponent(app, flights_df)
    delay_duration = DelayDurationComponent(flights_df)
    airline_performance = AirlinePerformanceComponent(app, flights_df, airlines_df)
    carrier_market_comparison = CarrierMarketComparisonComponent(app, flights_df, geojson_path)
    flight_distribution_component = FlightDistributionComponent(app, flights_df, states_df, geojson_path)

    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Flight Analysis Dashboard",
                    className="text-center text-primary mb-4 mt-4"))
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Flight Distribution Comparison"),
                    dbc.CardBody(
                        flight_distribution_component.create_component()
                    )
                ], className="mb-4")
            ], width=12, lg=6),
        ]),
         dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Carrier Market Comparison"),
                    dbc.CardBody(
                        carrier_market_comparison.create_component()
                    )
                ], className="mb-4")
            ], width=12, lg=6),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Flight Delays Duration"),
                    dbc.CardBody(
                        delay_duration.create_component()
                    )
                ], className="mb-4")
            ], width=12, lg=6),
        ]),
         dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Carrier Delays Comparison"),
                    dbc.CardBody(
                        airline_performance.create_component()
                    )
                ], className="mb-4")
            ], width=12, lg=6),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Flight Delays Distribution"),
                    dbc.CardBody(
                        delay_dist.create_component()
                    )
                ], className="mb-4")
            ], width=12, lg=6),
        ]),
         dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Flights Distribution by Time Period"),
                    dbc.CardBody(
                        time_dist.create_component()
                    )
                ], className="mb-4")
            ], width=12, lg=6)
        ]),
        dbc.Row([
            dbc.Col(
                html.Footer(
                    "Flight Analysis Dashboard - Created with Dash",
                    className="text-center text-muted mb-4"
                )
            )
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Number of flights per state between 2015 and 2020"),
                    dbc.CardBody(
                        html.Iframe(
                            srcDoc=open("./map/flight_per_state.html","r").read(),
                            style={"width": "100%", "height": "600px", "border": "none"}                            
                        )
                    )
                ], className="mb-4")
            ], width=12)
        ]),
    ], fluid=True)


    return app

if __name__ == "__main__":
    app = main()
    app.run_server(debug=True, port=8050)