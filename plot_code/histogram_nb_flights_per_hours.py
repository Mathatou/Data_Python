import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import Marker
from plotly.io import write_html

def exec(df):
    df_minutes = df['DepTime'].apply(time_to_minutes)
    max_minutes = 1440
    
    histogram = go.Figure()
    
    # Add vertical regions for different time periods
    periods = [
        # Night periods
        {"x0": 0, "x1": 360, "name": "Night", "color": "#D4E6F1"},     
        {"x0": 1260, "x1": 1440, "name": "Night", "color": "#D4E6F1"}, 
        # Main day periods
        {"x0": 360, "x1": 660, "name": "Morning", "color": "#FCF3CF"}, 
        {"x0": 660, "x1": 1080, "name": "Afternoon", "color": "#FADBD8"}, 
        {"x0": 1080, "x1": 1260, "name": "Evening", "color": "#E8DAEF"}  
    ]
    
    # Add background regions
    for period in periods:
        histogram.add_vrect(
            x0=period["x0"], 
            x1=period["x1"],
            fillcolor=period["color"], 
            opacity=0.3,
            layer="below", 
            line_width=0,
            name=period["name"]
        )
    
    histogram.add_trace(go.Histogram(
        x=df_minutes,
        nbinsx=max_minutes,  
        marker=dict(
            color='#4682B4',  # Steel blue
            line=dict(width=0.1, color='white')
        ),
        name='Departures',
        hovertemplate="Time: %{x}<br>Flights: %{y}<extra></extra>"
    ))
    
    # Add period labels at the top
    annotations = [
        dict(x=180, y=1.1, text="Night (00:00-06:00)", showarrow=False, xref='x', yref='paper'),
        dict(x=510, y=1.1, text="Morning (06:00-11:00)", showarrow=False, xref='x', yref='paper'),
        dict(x=870, y=1.1, text="Afternoon (11:00-18:00)", showarrow=False, xref='x', yref='paper'),
        dict(x=1170, y=1.1, text="Evening (18:00-21:00)", showarrow=False, xref='x', yref='paper'),
        dict(x=1350, y=1.1, text="Night (21:00-24:00)", showarrow=False, xref='x', yref='paper')
    ]
    
    tick_vals = list(range(0, max_minutes + 1, 30))  # Ticks every 30 minutes
    tick_text = [minutes_to_time_str(val) for val in tick_vals]
    
    histogram.update_layout(
        title=dict(
            text="Flight Departure Distribution Throughout the Day",
            font=dict(size=24),
            y=0.95
        ),
        xaxis=dict(
            tickmode='array',
            tickvals=tick_vals,
            ticktext=tick_text,
            tickangle=45,
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.5)',
            title=dict(
                text="Departure Time",
                font=dict(size=16)
            )
        ),
        yaxis=dict(
            title=dict(
                text="Number of Flights",
                font=dict(size=16)
            ),
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.5)'
        ),
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white"),
        showlegend=False,
        margin=dict(t=120, l=80, r=40, b=80),  # Increased top margin for period labels
        height=700,  # Made plot taller
        annotations=annotations  # Added period labels
    )
    
    return histogram




# Convert time to minutes
def time_to_minutes(time):
    # Handle NaN values
    if pd.isna(time):
        return np.nan
    
    # Convert to string and pad with zeros if needed
    time_str = str(int(time)).zfill(4)
    
    # Extract hours and minutes
    if len(time_str) <= 2:
        hours = 0
        minutes = int(time_str)
    else:
        hours = int(time_str[:-2])
        minutes = int(time_str[-2:])
    
    # Convert to total minutes
    total_minutes = hours * 60 + minutes
    return total_minutes

# Convert minutes back to time format for labels
def minutes_to_time_str(minutes):
    hours = int(minutes) // 60
    mins = int(minutes) % 60
    return f"{hours:02d}:{mins:02d}"
