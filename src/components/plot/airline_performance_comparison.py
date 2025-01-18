import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from dash.dependencies import Input, Output

class AirlinePerformanceComponent:
    def __init__(self, app, df, airlines_df):
        self.app = app
        self.df = df
        self.airlines_df = airlines_df
        self.component_id = 'airline-performance'
        self._register_callbacks()

    def create_component(self):
        """Creates the component layout"""
        return html.Div([
            dcc.Dropdown(
                id=f'{self.component_id}-num-carriers',
                options=[
                    {'label': 'Top 5', 'value': 5},
                    {'label': 'Top 10', 'value': 10},
                    {'label': 'All', 'value': -1}
                ],
                value=5,
                clearable=False,
                className='mb-3'
            ),
            dcc.Dropdown(
                id=f'{self.component_id}-sort-by',
                options=[
                    {'label': 'Average Delay', 'value': 'Avg_Delay'},
                    {'label': 'Cancellation Rate', 'value': 'Cancellation_Rate'}
                ],
                value='Avg_Delay',
                clearable=False,
                className='mb-3'
            ),
            dcc.Dropdown(
                id=f'{self.component_id}-sort-order',
                options=[
                    {'label': 'Most', 'value': 'desc'},
                    {'label': 'Least', 'value': 'asc'}
                ],
                value='desc',
                clearable=False,
                className='mb-3'
            ),
            dcc.Graph(id=f'{self.component_id}-graph')
        ])

    def _register_callbacks(self):
        """Registers callbacks"""
        @self.app.callback(
            Output(f'{self.component_id}-graph', 'figure'),
            [Input(f'{self.component_id}-num-carriers', 'value'),
             Input(f'{self.component_id}-sort-by', 'value'),
             Input(f'{self.component_id}-sort-order', 'value')]
        )
        def update_graph(num_carriers, sort_by, sort_order):
            return self._create_airline_performance_plot(num_carriers, sort_by, sort_order)

    def _create_airline_performance_plot(self, num_carriers, sort_by, sort_order):
        """Creates bar plot for airline performance comparison"""
        df = self.df.merge(self.airlines_df, left_on='Reporting_Airline', right_on='Carrier', how='left')
        
        airline_stats = df.groupby('CarrierName').agg({
            'DepDelay': ['mean', 'count'],  
            'Cancelled': 'sum'  
        }).reset_index()
        
        
        airline_stats.columns = ['CarrierName', 'Avg_Delay', 'Total_Flights', 'Cancelled_Flights']
        
        airline_stats['Cancellation_Rate'] = (airline_stats['Cancelled_Flights'] / airline_stats['Total_Flights'] * 100).round(2)
        
        airline_stats = airline_stats.sort_values(sort_by, ascending=(sort_order == 'asc'))
        
        if num_carriers > 0:
            airline_stats = airline_stats.head(num_carriers)
        
        bar_plot = go.Figure()
        
        bar_plot.add_trace(go.Bar(
            x=airline_stats['CarrierName'],
            y=airline_stats[sort_by],
            name=f'{sort_by.replace("_", " ")}',
            marker_color='#4682B4',  # Steel blue
            hovertemplate="<b>%{x}</b><br>" +
                         f"{sort_by.replace('_', ' ')}: %{{y:.1f}}<br>" +
                         "Total Flights: %{customdata[0]}<br>" +
                         "Cancellation Rate: %{customdata[1]}%<extra></extra>",
            customdata=airline_stats[['Total_Flights', 'Cancellation_Rate']].values
        ))
        
        bar_plot.update_layout(
            title=dict(
                text='Airline Performance Comparison',
                font=dict(size=24),
                y=0.95
            ),
            xaxis=dict(
                title=dict(
                    text="Airline",
                    font=dict(size=16)
                ),
                tickangle=45,  
                showgrid=False
            ),
            yaxis=dict(
                title=dict(
                    text=f"{sort_by.replace('_', ' ')}",
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
        
        bar_plot.add_annotation(
            text="Hover over bars to see detailed statistics including total flights and cancellation rates",
            xref="paper", yref="paper",
            x=0, y=1.1,
            showarrow=False,
            font=dict(size=12, color="gray")
        )
        
        return bar_plot