import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from dash.dependencies import Input, Output
from src.utils.time import format_time

class DelayDistributionComponent:
    def __init__(self, app, df):
        self.app = app
        self.df = df
        self.component_id = 'delay-distribution'
        self._register_callbacks()

    def create_component(self):
        return html.Div([
            dcc.Dropdown(
                id=f'{self.component_id}-dropdown',
                options=[
                    {'label': 'Time of Day', 'value': 'time'},
                    {'label': 'Day of Week', 'value': 'day'},
                    {'label': 'Month', 'value': 'month'},
                    {'label': 'Year', 'value': 'year'}
                ],
                value='time',
                clearable=False,
                className='mb-3'
            ),
            dcc.Graph(id=f'{self.component_id}-graph')
        ])

    def _register_callbacks(self):
        @self.app.callback(
            Output(f'{self.component_id}-graph', 'figure'),
            [Input(f'{self.component_id}-dropdown', 'value')]
        )
        def update_graph(selected_period):
            if selected_period == 'time':
                return self._create_time_distribution()
            elif selected_period == 'day':
                return self._create_daily_distribution()
            elif selected_period == 'month':
                return self._create_monthly_distribution()
            else:  
                return self._create_yearly_distribution()

    def _get_delay_categories(self):
        delayed_flights = self.df[(self.df['DepDelay'] >= 15) & (self.df['DepDelay'] < 220)]
        
        return {
            'minor': delayed_flights[(delayed_flights['DepDelay'] >= 15) & 
                                   (delayed_flights['DepDelay'] <= 30)],
            'significant': delayed_flights[(delayed_flights['DepDelay'] > 30) & 
                                        (delayed_flights['DepDelay'] <= 120)],
            'major': delayed_flights[(delayed_flights['DepDelay'] > 120) & 
                                   (delayed_flights['DepDelay'] <= 240)],
            'severe': delayed_flights[delayed_flights['DepDelay'] > 240]
        }

    def _create_time_distribution(self):
        """Creates histogram for Trends in Delays Over the Day"""
        delays = self._get_delay_categories()
        fig = go.Figure()
        
        all_times = pd.date_range("00:00", "23:55", freq="5min").time
        
        
        
        delay_configs = [
            ('minor', 'Minor Delays (15-30 min)', '#90EE90'),
            ('significant', 'Significant Delays (30-120 min)', '#FFD700'),
            ('major', 'Major Delays (120-240 min)', '#FFA500'),
            ('severe', 'Severe Delays (>240 min)', '#FF4500')
        ]
        
        for delay_type, name, color in delay_configs:
            df_time = delays[delay_type].copy()
            df_time['TimeOfDay'] = df_time['CRSDepTime'].apply(format_time)
            time_counts = df_time.groupby('TimeOfDay').size()
            
            time_counts = time_counts.reindex(all_times, fill_value=0)
            
            fig.add_trace(go.Bar(
                x=[t.strftime('%H:%M') for t in time_counts.index],
                y=time_counts.values,
                name=name,
                marker_color=color
            ))

        tick_vals = [t.strftime('%H:%M') for t in pd.date_range("00:00", "23:59", freq="30min").time]

        self._update_layout(fig, "Distribution of Delays Throughout the Day",
                        "Scheduled Departure Time", "Number of Flights",
                        stack=True, tick_vals=tick_vals)
        
     
        
        return fig

    def _create_daily_distribution(self):
        """Creates stacked bar chart for delay distribution by day"""
        delays = self._get_delay_categories()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        fig = go.Figure()
        
        for delay_type, name, color in [
            ('minor', 'Minor Delays (15-30 min)', '#90EE90'),
            ('significant', 'Significant Delays (30-120 min)', '#FFD700'),
            ('major', 'Major Delays (120-240 min)', '#FFA500'),
            ('severe', 'Severe Delays (>240 min)', '#FF4500')
        ]:
            df_daily = delays[delay_type].copy()
            df_daily['DayOfWeek'] = pd.to_datetime(
                df_daily['Year'].astype(str) + '-' + 
                df_daily['Month'].astype(str) + '-' + 
                df_daily['DayofMonth'].astype(str)
            ).dt.dayofweek
            
            day_counts = df_daily['DayOfWeek'].value_counts().reindex(range(7)).fillna(0)
            
            fig.add_trace(go.Bar(
                x=days,
                y=day_counts.values,
                name=name,
                marker_color=color
            ))
        
        self._update_layout(fig, "Distribution of Flight Delays by Day of Week",
                          "Day of Week", "Number of Flights", stack=True)
        return fig

    def _create_monthly_distribution(self):
        """Creates stacked bar chart for delay distribution by month"""
        delays = self._get_delay_categories()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        fig = go.Figure()
        
        for delay_type, name, color in [
            ('minor', 'Minor Delays (15-30 min)', '#90EE90'),
            ('significant', 'Significant Delays (30-120 min)', '#FFD700'),
            ('major', 'Major Delays (120-240 min)', '#FFA500'),
            ('severe', 'Severe Delays (>240 min)', '#FF4500')
        ]:
            month_counts = delays[delay_type]['Month'].value_counts().reindex(range(1, 13)).fillna(0)
            
            fig.add_trace(go.Bar(
                x=months,
                y=month_counts.values,
                name=name,
                marker_color=color
            ))
        
        self._update_layout(fig, "Distribution of Flight Delays by Month",
                          "Month", "Number of Flights", stack=True)
        return fig

    def _create_yearly_distribution(self):
        """Creates stacked bar chart for delay distribution by year"""
        delays = self._get_delay_categories()
        
        fig = go.Figure()
        
        for delay_type, name, color in [
            ('minor', 'Minor Delays (15-30 min)', '#90EE90'),
            ('significant', 'Significant Delays (30-120 min)', '#FFD700'),
            ('major', 'Major Delays (120-240 min)', '#FFA500'),
            ('severe', 'Severe Delays (>240 min)', '#FF4500')
        ]:
            year_counts = delays[delay_type]['Year'].value_counts().sort_index()
            
            fig.add_trace(go.Bar(
                x=year_counts.index,
                y=year_counts.values,
                name=name,
                marker_color=color
            ))
        
        self._update_layout(fig, "Distribution of Flight Delays by Year",
                          "Year", "Number of Flights", stack=True)
        return fig

    def _update_layout(self, fig, title, xaxis_title, yaxis_title, stack=False, tick_vals=None):
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
        
        if stack:
            layout_dict['barmode'] = 'stack'
        
        if tick_vals is not None:  
            layout_dict['xaxis']['tickmode'] = 'array'
            layout_dict['xaxis']['tickvals'] = tick_vals
            layout_dict['xaxis']['ticktext'] = tick_vals 
            layout_dict['xaxis']['tickangle'] = 45
        
        fig.update_layout(layout_dict)