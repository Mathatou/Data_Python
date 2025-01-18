import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

def create_navbar(app):
    navbar = dbc.NavbarSimple(
        id="navbar", 
        children=[
            dbc.NavItem(dbc.NavLink("Delay Analysis", href="/delay-analysis", id="delay-analysis-link")),
            dbc.NavItem(dbc.NavLink("Route Analysis", href="/route-analysis", id="route-analysis-link")),
            dbc.NavItem(dbc.NavLink("Airline Performance", href="/airline-performance", id="airline-performance-link")),
            dbc.NavItem(dbc.NavLink("Temporal Models", href="/temporal-models", id="temporal-models-link")),
        ],
        brand="Flight Analysis Dashboard",
        brand_href="/",
        color="secondary",
        dark=True,
        className="mb-4"
    )

    @app.callback(
        [Output("delay-analysis-link", "style"),
         Output("route-analysis-link", "style"),
         Output("airline-performance-link", "style"),
         Output("temporal-models-link", "style")],
        [Input("url", "pathname")]
    )
    def update_navbar_style(pathname):
        default_style = {"fontWeight": "normal", "color": "rgba(255, 255, 255, 0.5)"}

        active_style = {"fontWeight": "bold", "color": "white"}

        delay_style = active_style if pathname == "/delay-analysis" else default_style
        route_style = active_style if pathname == "/route-analysis" else default_style
        airline_style = active_style if pathname == "/airline-performance" else default_style
        temporal_style = active_style if pathname == "/temporal-models" else default_style

        return delay_style, route_style, airline_style, temporal_style

    return navbar