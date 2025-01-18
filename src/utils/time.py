import pandas as pd


def format_time(time):
    """Converts time in HHMM format to a time object, handling NaN values."""
    if pd.isna(time): 
        return None
    time_str = str(int(time)).zfill(4)  
    hours = int(time_str[:2]) 
    minutes = int(time_str[-2:]) 
    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
        return None
    return pd.Timestamp(year=2000, month=1, day=1, hour=hours, minute=minutes).time()