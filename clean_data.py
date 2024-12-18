import pandas as pd
import os

def main():
    extracted_csv_file = "./extracted_csv_file/"
    clean_data = "./csv"
    os.makedirs(clean_data, exist_ok=True)
    
    ds = pd.read_csv(extracted_csv_file + "airline_2m.csv",encoding='latin1')
    if 'Year' not in ds.columns:
        print("Error")
        return 
    if ds.empty:
        print("Error")
        return
    
    
    filtered_ds = ds[(ds['Year']>= 2015) & (ds['Year']<=2020)]
    # List of columns to drop
    columns_to_drop = [
    'Div5TailNum', 'Div5WheelsOff', 'Div5LongestGTime', 'Div5TotalGTime', 'Div5AirportSeqID',
    'Div2Airport', 'Div2AirportID', 'Div2AirportSeqID', 'Div2WheelsOn', 'Div2TotalGTime',
    'Div2LongestGTime', 'Div2WheelsOff', 'Div2TailNum', 'Div3Airport', 'Div3AirportID',
    'Div3AirportSeqID', 'Div3WheelsOn', 'Div3TotalGTime', 'Div3LongestGTime', 'Div3WheelsOff',
    'Div3TailNum', 'Div4Airport', 'Div4AirportID', 'Div4AirportSeqID', 'Div4WheelsOn',
    'Div4TotalGTime', 'Div4LongestGTime', 'Div4WheelsOff', 'Div4TailNum', 'Div5Airport',
    'Div5AirportID', 'Div5WheelsOn',
    'DivAirportLandings', 'DivReachedDest', 'DivActualElapsedTime', 'DivArrDelay',
    'DivDistance', 'Div1Airport', 'Div1AirportID', 'Div1AirportSeqID', 'Div1WheelsOn',
    'Div1TotalGTime', 'Div1LongestGTime', 'Div1WheelsOff', 'Div1TailNum','OriginStateName',
    'DestStateName'
]

    # Drop the columns
    filtered_ds = filtered_ds.drop(columns=columns_to_drop, errors='ignore')

        
        
    filtered_ds.to_csv(os.path.join(clean_data,"cleaned_csv.csv"),index=False)
    
if __name__ == '__main__':
    main()