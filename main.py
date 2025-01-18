from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output  
from src.pages.delay_analysis import create_layout as create_delay_analysis_layout
from src.pages.route_analysis import create_layout as create_route_analysis_layout
from src.pages.airline_performance import create_layout as create_airline_performance_layout
from src.pages.temporal_models import create_layout as create_temporal_models_layout
from src.components.layout.navbar import create_navbar
from src.components.layout.footer import create_footer
import pandas as pd
from csv_utils.extract_csv import extract_if_needed
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO], suppress_callback_exceptions=True)

extract_if_needed()

flights_df = pd.read_csv("data/csv/flights.csv", encoding='latin1')
states_df = pd.read_csv("data/csv/states.csv", encoding='latin1')
geojson_path = "data/geojson/geous.geojson"
airlines_df = pd.read_csv("data/csv/airlines.csv", encoding='latin1')

delay_analysis_layout = create_delay_analysis_layout(app, flights_df)
route_analysis_layout = create_route_analysis_layout(app, flights_df, states_df, geojson_path)
airline_performance_layout = create_airline_performance_layout(app, flights_df, airlines_df, geojson_path)
temporal_models_layout = create_temporal_models_layout(app, flights_df)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False), 
    create_navbar(app),  
    html.Div(id='page-content'),  
    create_footer() 
])

@app.callback(
    Output('page-content', 'children'), 
    [Input('url', 'pathname')]  
)
def display_page(pathname):
    if pathname == '/delay-analysis':
        return delay_analysis_layout
    elif pathname == '/route-analysis':
        return route_analysis_layout
    elif pathname == '/airline-performance':
        return airline_performance_layout
    elif pathname == '/temporal-models':
        return temporal_models_layout
    else:
        return delay_analysis_layout 

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)