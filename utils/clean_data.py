import pandas as pd
import os

def main():
    final_folder = "./csv/"
    os.makedirs(final_folder, exist_ok=True)
    

    airline_prefiltered = "airline_2m.csv"
    airport_prefiltered = "airports.csv"
    flights_prefiltered = "airline_2m.csv"
    
    # Read the CSV file
    try:
        airport_df = pd.read_csv(final_folder + airport_prefiltered, encoding='latin1')
        airline_df = pd.read_csv(final_folder + airline_prefiltered,encoding='latin1')
        flights_df = pd.read_csv(final_folder + flights_prefiltered,encoding='latin1')

    except FileNotFoundError:
        print("File not found.")
        return

    if 'Year' not in airline_df.columns:
        print("Error")
        return 
    if airline_df.empty:
        print("Error")
        return
    
    
    filtered_ds = airline_df[(airline_df['Year']>= 2015) & (airline_df['Year']<=2020)]
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
    'DestStateName','Flights'
    ]

    # Drop the columns
    filtered_ds = filtered_ds.drop(columns=columns_to_drop, errors='ignore')

    
    final_name = "flights.csv"
    filtered_ds.to_csv(os.path.join(final_folder, final_name),index=False)

    os.remove(final_folder + airline_prefiltered)
    # File name

    # Clean flights
    # Define unwanted airport types
    unwanted_types = ['heliport', 'closed', 'seaplane_base', 'balloonport']

    # Perform an inner merge between flights_df and airport_df on OriginAirportID and id
    merged_df = flights_df.merge(
        airport_df[['id', 'type']],  # Select only necessary columns from airport_df
        left_on='OriginAirportID',
        right_on='id',
        how='left'
    )

    # Filter out rows where the airport type is in the unwanted list
    filtered_flights = merged_df[~merged_df['type'].isin(unwanted_types)]

    # Drop the 'type' and 'id' columns (optional)
    filtered_flights = filtered_flights.drop(columns=['type', 'id'])
    filtered_flights.to_csv(os.path.join(final_folder+"flights.csv"),index=False)
    
    # Clean airports
    
    # Check if 'type' column exists
    if 'type' not in airport_df:
        print("Error: 'type' column not found in the dataset.")
        return

    # Drop rows with specific 'type' values
    airport_df = airport_df[
        ~airport_df['type'].isin(["heliport", "closed", "seaplane_base", "balloonport"])
    ]

    # Save the cleaned dataset to the same file
    cleaned_file = final_folder + "airports.csv"
    airport_df.to_csv(cleaned_file, index=False, encoding='utf-8')
    print(f"Cleaned data saved to {cleaned_file}")


if __name__ == '__main__':
    main()