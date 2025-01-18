import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

class DelayDurationComponent:
    def __init__(self, df):
        self.df = df
        self.component_id = 'delay-duration'
        self.max_delay = None

    def create_component(self):
        """Creates the component layout"""
        fig = self.create_minutes_duration()
        return html.Div([
            dcc.Graph(id=f'{self.component_id}-graph', figure=fig)
        ])

    def _get_delay_categories(self):
        """Helper function to categorize delays"""
        delayed_flights = self.df[(self.df['DepDelay'] >= 15) & (self.df['DepDelay'] < 220)]
        return delayed_flights

    def create_minutes_duration(self):
        """Creates histogram for delay duration in minutes"""
        delayed_flights = self._get_delay_categories()
        self.max_delay = int(np.ceil(delayed_flights['DepDelay'].max()))
        
        fig = go.Figure()
        
        delay_categories = [
            {'name': 'Minor Delays (15-30 min)', 'range': [15, 30], 'color': '#90EE90'},
            {'name': 'Significant Delays (30-120 min)', 'range': [30, 120], 'color': '#FFD700'},
            {'name': 'Major Delays (120-240 min)', 'range': [120, 240], 'color': '#FFA500'},
            {'name': 'Severe Delays (>240 min)', 'range': [240, self.max_delay], 'color': '#FF4500'}
        ]

        for category in delay_categories:
            fig.add_vrect(
                x0=category['range'][0],
                x1=category['range'][1],
                fillcolor=category['color'],
                opacity=0.3,
                layer="below",
                line_width=0,
                name=category['name']
            )

        fig.add_trace(go.Histogram(
            x=delayed_flights['DepDelay'],
            xbins=dict(start=15, end=self.max_delay, size=1),
            marker_line=dict(width=0.1, color='black'),
            hovertemplate="Delay: %{x} min<br>Flights: %{y}<extra></extra>"
        ))

        annotations = [
            dict(x=22.5, y=1.1, text="Minor (15-30 min)", showarrow=False, xref='x', yref='paper'),
            dict(x=75, y=1.1, text="Significant (30-120 min)", showarrow=False, xref='x', yref='paper'),
            dict(x=180, y=1.1, text="Major (120-240 min)", showarrow=False, xref='x', yref='paper'),
            dict(x=240, y=1.1, text="Severe (>240 min)", showarrow=False, xref='x', yref='paper')
        ]

        self._update_layout(fig, "Distribution of Flight Delays by Severity",
                          "Departure Delay (Minutes)", "Number of Flights",
                          annotations=annotations)
        return fig

    def _update_layout(self, fig, title, xaxis_title, yaxis_title, annotations=None):
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
                gridcolor='rgba(211, 211, 211, 0.5)',
                range=[14, self.max_delay], 
                dtick=5,  
                tickangle=-45,  
                tickmode='linear',  
                tick0=15,  
                tickfont=dict(size=12) 
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
            template="plotly_white",
            showlegend=False,
            height=700,
            margin=dict(t=120, l=80, r=40, b=80)
        )
        
        if annotations:
            layout_dict['annotations'] = annotations
            
        fig.update_layout(layout_dict)