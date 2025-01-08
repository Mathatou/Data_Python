import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import Marker
from plotly.io import write_html

def exec(df):
    # Read airlines data
    airlines_df = pd.read_csv("./csv/airlines.csv", encoding='latin1')
    
    # Merge flight data with airlines data
    df = df.merge(airlines_df, left_on='Reporting_Airline', right_on='Carrier', how='left')
    
    # Calculate performance metrics for each airline
    airline_stats = df.groupby('CarrierName').agg({
        'DepDelay': ['mean', 'count'],  # Average delay and number of flights
        'Cancelled': 'sum'  # Number of cancelled flights
    }).reset_index()
    
    # Flatten column names
    airline_stats.columns = ['CarrierName', 'Avg_Delay', 'Total_Flights', 'Cancelled_Flights']
    
    # Calculate cancellation rate
    airline_stats['Cancellation_Rate'] = (airline_stats['Cancelled_Flights'] / airline_stats['Total_Flights'] * 100).round(2)
    
    # Sort by average delay
    airline_stats = airline_stats.sort_values('Avg_Delay', ascending=False)
    
    bar_plot = go.Figure()
    
    # Add bars for average delay
    bar_plot.add_trace(go.Bar(
        x=airline_stats['CarrierName'],
        y=airline_stats['Avg_Delay'],
        name='Average Delay (minutes)',
        marker_color='#4682B4',  # Steel blue
        hovertemplate="<b>%{x}</b><br>" +
                     "Average Delay: %{y:.1f} minutes<br>" +
                     "Total Flights: %{customdata[0]}<br>" +
                     "Cancellation Rate: %{customdata[1]}%<extra></extra>",
        customdata=airline_stats[['Total_Flights', 'Cancellation_Rate']].values
    ))
    
    # Update layout with improved styling
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
            tickangle=45,  # Angle the airline names for better readability
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text="Average Delay (minutes)",
                font=dict(size=16)
            ),
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.5)'
        ),
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white"),
        margin=dict(t=100, l=80, r=40, b=120),  # Increased bottom margin for angled labels
        height=700  # Taller plot for better readability
    )
    
    # Add a comment about data interpretation
    bar_plot.add_annotation(
        text="Hover over bars to see detailed statistics including total flights and cancellation rates",
        xref="paper", yref="paper",
        x=0, y=1.1,
        showarrow=False,
        font=dict(size=12, color="gray")
    )
    
    bar_plot.show()