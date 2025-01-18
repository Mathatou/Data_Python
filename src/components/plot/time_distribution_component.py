import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from dash.dependencies import Input, Output
from src.utils.time import format_time

class TimeDistributionComponent:
    def __init__(self, app, df):
        self.app = app 
        self.df = df
        self.component_id = 'time-distribution'
        self._register_callbacks()  

    def create_component(self):
        """Creates the component layout"""
        return html.Div([
            dcc.Dropdown(
                id=f'{self.component_id}-dropdown',
                options=[
                    {'label': 'Minutes', 'value': 'minutes'},
                    {'label': 'Days', 'value': 'days'},
                    {'label': 'Months', 'value': 'months'},
                    {'label': 'Years', 'value': 'years'}
                ],
                value='minutes',
                clearable=False,
                className='mb-3'
            ),
            dcc.Graph(id=f'{self.component_id}-graph')
        ])

    def _register_callbacks(self):
        """Registers callbacks"""
        @self.app.callback(
            Output(f'{self.component_id}-graph', 'figure'),
            [Input(f'{self.component_id}-dropdown', 'value')]
        )
        def update_graph(selected_period):
            if selected_period == 'minutes':
                return self._create_hourly_distribution()
            elif selected_period == 'days':
                return self._create_daily_distribution()
            elif selected_period == 'months':
                return self._create_monthly_distribution()
            else:  
                return self._create_yearly_distribution()

    def _create_hourly_distribution(self):
        """Creates histogram for hourly distribution aggregated every five minutes using time-based intervals"""
        time_str = self.df['DepTime'].apply(format_time).astype(str).replace('NaT', '')
        df_time = pd.to_datetime('2000-01-01 ' + time_str, errors='coerce').dropna()
        
        fig = go.Figure()
        
        periods = [
            {"x0": pd.to_datetime("2000-01-01 00:00"), "x1": pd.to_datetime("2000-01-01 06:00"), "name": "Night", "color": "#D4E6F1"},
            {"x0": pd.to_datetime("2000-01-01 21:00"), "x1": pd.to_datetime("2000-01-01 23:59"), "name": "Night", "color": "#D4E6F1"},
            {"x0": pd.to_datetime("2000-01-01 06:00"), "x1": pd.to_datetime("2000-01-01 11:00"), "name": "Morning", "color": "#FCF3CF"},
            {"x0": pd.to_datetime("2000-01-01 11:00"), "x1": pd.to_datetime("2000-01-01 18:00"), "name": "Afternoon", "color": "#FADBD8"},
            {"x0": pd.to_datetime("2000-01-01 18:00"), "x1": pd.to_datetime("2000-01-01 21:00"), "name": "Evening", "color": "#E8DAEF"}
        ]
        
        for period in periods:
            fig.add_vrect(
                x0=period["x0"],
                x1=period["x1"],
                fillcolor=period["color"],
                opacity=0.3,
                layer="below",
                line_width=0,
                name=period["name"]
            )
        
        fig.add_trace(go.Histogram(
            x=df_time,
            xbins=dict(start=pd.to_datetime("2000-01-01 00:00"), end=pd.to_datetime("2000-01-01 23:59"), size=5*60*1000),
            marker_color='#4682B4',
            name='Departures',
            hovertemplate="Time: %{x}<br>Flights: %{y}<extra></extra>"
        ))
        
        annotations = [
            dict(x=pd.to_datetime("2000-01-01 03:00"), y=1.1, text="Night (00:00-06:00)", showarrow=False, xref='x', yref='paper'),
            dict(x=pd.to_datetime("2000-01-01 08:30"), y=1.1, text="Morning (06:00-11:00)", showarrow=False, xref='x', yref='paper'),
            dict(x=pd.to_datetime("2000-01-01 14:30"), y=1.1, text="Afternoon (11:00-18:00)", showarrow=False, xref='x', yref='paper'),
            dict(x=pd.to_datetime("2000-01-01 19:30"), y=1.1, text="Evening (18:00-21:00)", showarrow=False, xref='x', yref='paper'),
            dict(x=pd.to_datetime("2000-01-01 22:30"), y=1.1, text="Night (21:00-24:00)", showarrow=False, xref='x', yref='paper')
        ]
        
        tick_vals = pd.date_range("2000-01-01 00:00", "2000-01-01 23:59", freq="30min")
        
        self._update_layout(fig, "Flight Departure Distribution Throughout the Day", 
                            "Departure Time", "Number of Flights", annotations, tick_vals, xaxis_type='date')
        return fig

        
    def _create_daily_distribution(self):
        """Creates bar plot for daily distribution"""
        df_daily = self.df.copy()
        
        df_daily['Date'] = pd.to_datetime(
            df_daily['Year'].astype(str) + '-' + 
            df_daily['Month'].astype(str) + '-' + 
            df_daily['DayofMonth'].astype(str),
            errors='coerce'
        )
        
        df_daily = df_daily.dropna(subset=['Date'])
        
        df_daily['DayOfWeek'] = df_daily['Date'].dt.dayofweek
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = df_daily['DayOfWeek'].value_counts().sort_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=days,
            y=day_counts.values,
            marker_color='#4682B4',
            name='Departures'
        ))
        
        self._update_layout(fig, "Flight Distribution by Day of Week",
                            "Day of Week", "Number of Flights")
        return fig

    def _create_monthly_distribution(self):
        """Creates bar plot for monthly distribution"""
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        month_counts = self.df['Month'].value_counts().sort_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=months,
            y=month_counts.values,
            marker_color='#4682B4',
            name='Departures'
        ))
        
        self._update_layout(fig, "Flight Distribution by Month",
                            "Month", "Number of Flights")
        return fig

    def _create_yearly_distribution(self):
        """Creates bar plot for yearly distribution"""
        year_counts = self.df['Year'].value_counts().sort_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=year_counts.index,
            y=year_counts.values,
            marker_color='#4682B4',
            name='Departures'
        ))
        
        self._update_layout(fig, "Flight Distribution by Year",
                            "Year", "Number of Flights")
        return fig
    
    def _update_layout(self, fig, title, xaxis_title, yaxis_title, annotations=None, tick_vals=None, xaxis_type=None):
        """Updates the layout of the figure"""
        layout_dict = dict(
            title=dict(
                text=title,
                font=dict(size=24),
                y=0.95
            ),
            xaxis=dict(
                title=dict(
                    text=xaxis_title,
                    font=dict(size=16)
                ),
                showgrid=True,
                gridcolor='rgba(211, 211, 211, 0.5)'
            ),
            yaxis=dict(
                title=dict(
                    text=yaxis_title,
                    font=dict(size=16)
                ),
                showgrid=True,
                gridcolor='rgba(211, 211, 211, 0.5)'
            ),
            plot_bgcolor='white',
            hoverlabel=dict(bgcolor="white"),
            showlegend=False,
            margin=dict(t=120, l=80, r=40, b=80),
            height=700
        )
        
        if annotations:
            layout_dict['annotations'] = annotations
        
        if tick_vals is not None:
            layout_dict['xaxis']['tickmode'] = 'array'
            layout_dict['xaxis']['tickvals'] = tick_vals
            layout_dict['xaxis']['ticktext'] = [t.strftime('%H:%M') for t in tick_vals] if xaxis_type == 'date' else tick_vals
            layout_dict['xaxis']['tickangle'] = 45
        
        if xaxis_type:
            layout_dict['xaxis']['type'] = xaxis_type
        
        fig.update_layout(layout_dict)