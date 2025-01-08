import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import Marker
from plotly.io import write_html

def exec(df):
    # Filter for delays between 15 and 220 minutes
    delayed_flights = df[(df['DepDelay'] >= 15) & (df['DepDelay'] < 220)]
    
    # Create separate DataFrames for each category
    minor_delays = delayed_flights[(delayed_flights['DepDelay'] >= 15) & (delayed_flights['DepDelay'] <= 30)]
    significant_delays = delayed_flights[(delayed_flights['DepDelay'] > 30) & (delayed_flights['DepDelay'] <= 120)]
    major_delays = delayed_flights[(delayed_flights['DepDelay'] > 120) & (delayed_flights['DepDelay'] <= 240)]
    severe_delays = delayed_flights[delayed_flights['DepDelay'] > 240]
    
    max_delay = int(np.ceil(delayed_flights['DepDelay'].max()))
    
    histogram = go.Figure()
    
    # Add a trace for each category
    histogram.add_trace(go.Histogram(
        x=minor_delays['DepDelay'],
        name='Minor Delays (15-30 min)',
        nbinsx=max_delay,
        marker=dict(color='#90EE90', line=dict(width=1, color='black'))  # Light green
    ))
    
    histogram.add_trace(go.Histogram(
        x=significant_delays['DepDelay'],
        name='Significant Delays (30-120 min)',
        nbinsx=max_delay,
        marker=dict(color='#FFD700', line=dict(width=1, color='black'))  # Gold
    ))
    
    histogram.add_trace(go.Histogram(
        x=major_delays['DepDelay'],
        name='Major Delays (120-240 min)',
        nbinsx=max_delay,
        marker=dict(color='#FFA500', line=dict(width=1, color='black'))  # Orange
    ))
    
    histogram.add_trace(go.Histogram(
        x=severe_delays['DepDelay'],
        name='Severe Delays (>240 min)',
        nbinsx=max_delay,
        marker=dict(color='#FF4500', line=dict(width=1, color='black'))  # Red-orange
    ))
    
    histogram.update_layout(
        title="Distribution of over 345 662 Flight Delays by Severity",
        xaxis_title="Departure Delay (Minutes)",
        yaxis_title="Number of Flights",
        template="plotly_white",
        barmode='stack', 
        showlegend=True,
        xaxis=dict(
            dtick=1,
            tick0=14,
            range=[14, max_delay]
        )
    )
    
    
    return histogram

