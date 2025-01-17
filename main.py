import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from plot_code.airline_delay_comparison import exec as airline_delay_plot
from plot_code.histogram_nb_flights_per_delay import exec as flights_delay_plot
from plot_code.time_distribution_component import TimeDistributionComponent  

def main():
    df = pd.read_csv("./csv/flights.csv", encoding='latin1')
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    delay_comparison = airline_delay_plot(df)
    flights_delay = flights_delay_plot(df)
    time_dist = TimeDistributionComponent(app, df)

    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Flight Analysis Dashboard",
                    className="text-center text-primary mb-4 mt-4"))
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Flight Delays Distribution"),
                    dbc.CardBody(
                        dcc.Graph(figure=flights_delay)
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
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Airline Performance Comparison"),
                    dbc.CardBody(
                        dcc.Graph(figure=delay_comparison)
                    )
                ], className="mb-4")
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col(
                html.Footer(
                    "Flight Analysis Dashboard - Created with Dash",
                    className="text-center text-muted mb-4"
                )
            )
        ])
    ], fluid=True)


    return app

if __name__ == "__main__":
    app = main()
    app.run_server(debug=True, port=8050)