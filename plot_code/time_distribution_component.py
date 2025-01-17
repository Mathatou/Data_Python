import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from dash.dependencies import Input, Output

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
                    {'label': 'Hours', 'value': 'hours'},
                    {'label': 'Days', 'value': 'days'},
                    {'label': 'Months', 'value': 'months'},
                    {'label': 'Years', 'value': 'years'}
                ],
                value='hours',
                clearable=False,
                className='mb-3'
            ),
            dcc.Graph(id=f'{self.component_id}-graph')
        ])

    def _register_callbacks(self):
        """Registers  callbacks"""
        @self.app.callback(
            Output(f'{self.component_id}-graph', 'figure'),
            [Input(f'{self.component_id}-dropdown', 'value')]
        )
        def update_graph(selected_period):
            if selected_period == 'hours':
                return self._create_hourly_distribution()
            elif selected_period == 'days':
                return self._create_daily_distribution()
            elif selected_period == 'months':
                return self._create_monthly_distribution()
            else:  # years
                return self._create_yearly_distribution()

    def _create_hourly_distribution(self):
        """Creates histogram for hourly distribution """
        df_minutes = self.df['DepTime'].apply(self._time_to_minutes)
        max_minutes = 1440
        fig = go.Figure()
        
        periods = [
            {"x0": 0, "x1": 360, "name": "Night", "color": "#D4E6F1"},
            {"x0": 1260, "x1": 1440, "name": "Night", "color": "#D4E6F1"},
            {"x0": 360, "x1": 660, "name": "Morning", "color": "#FCF3CF"},
            {"x0": 660, "x1": 1080, "name": "Afternoon", "color": "#FADBD8"},
            {"x0": 1080, "x1": 1260, "name": "Evening", "color": "#E8DAEF"}
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
            x=df_minutes,
            nbinsx=max_minutes,
            marker=dict(
                color='#4682B4',
                line=dict(width=0.1, color='white')
            ),
            name='Departures',
            hovertemplate="Time: %{x}<br>Flights: %{y}<extra></extra>"
        ))
        
        annotations = [
            dict(x=180, y=1.1, text="Night (00:00-06:00)", showarrow=False, xref='x', yref='paper'),
            dict(x=510, y=1.1, text="Morning (06:00-11:00)", showarrow=False, xref='x', yref='paper'),
            dict(x=870, y=1.1, text="Afternoon (11:00-18:00)", showarrow=False, xref='x', yref='paper'),
            dict(x=1170, y=1.1, text="Evening (18:00-21:00)", showarrow=False, xref='x', yref='paper'),
            dict(x=1350, y=1.1, text="Night (21:00-24:00)", showarrow=False, xref='x', yref='paper')
        ]
        
        tick_vals = list(range(0, max_minutes + 1, 30))
        tick_text = [self._minutes_to_time_str(val) for val in tick_vals]
        
        self._update_layout(fig, "Flight Departure Distribution Throughout the Day", 
                          "Departure Time", "Number of Flights", annotations, tick_vals, tick_text)
        return fig

    def _create_daily_distribution(self):
        """Creates bar plot for daily distribution"""
        df_daily = self.df.copy()
        df_daily['DayOfWeek'] = pd.to_datetime(
            df_daily['Year'].astype(str) + '-' + 
            df_daily['Month'].astype(str) + '-' + 
            df_daily['DayofMonth'].astype(str)
        ).dt.dayofweek
        
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

    def _update_layout(self, fig, title, xaxis_title, yaxis_title, 
                      annotations=None, tick_vals=None, tick_text=None):
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
        
        if tick_vals and tick_text:
            layout_dict['xaxis']['tickmode'] = 'array'
            layout_dict['xaxis']['tickvals'] = tick_vals
            layout_dict['xaxis']['ticktext'] = tick_text
            layout_dict['xaxis']['tickangle'] = 45
        
        fig.update_layout(layout_dict)

    @staticmethod
    def _time_to_minutes(time):
        """Converts time to minutes"""
        if pd.isna(time):
            return np.nan
        time_str = str(int(time)).zfill(4)
        if len(time_str) <= 2:
            hours = 0
            minutes = int(time_str)
        else:
            hours = int(time_str[:-2])
            minutes = int(time_str[-2:])
        return hours * 60 + minutes

    @staticmethod
    def _minutes_to_time_str(minutes):
        """Converts minutes to time string"""
        hours = int(minutes) // 60
        mins = int(minutes) % 60
        return f"{hours:02d}:{mins:02d}"