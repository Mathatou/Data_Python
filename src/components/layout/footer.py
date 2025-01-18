import dash_bootstrap_components as dbc
from dash import html

def create_footer():
    return html.Footer(
        dbc.Container([
            html.Hr(),  
            html.P(
                "© 2025 Flight Analysis Dashboard",
                className="text-center text-muted mb-2"
            ),
            html.P(
                "Created by: Mathias AUBRY and Cyprien BOSCHER",
                className="text-center text-muted"
            ),
        ]),
        className="mt-4 p-4 bg-light" 
    )