import pandas as pd

import plot_code.airline_delay_comparison
import plot_code.histogram_nb_flights_per_delay
import plot_code.histogram_nb_flights_per_hours

def main():
    df = pd.read_csv("./csv/flights.csv", encoding='latin1')
    plot_code.histogram_nb_flights_per_delay.exec(df)
    plot_code.histogram_nb_flights_per_hours.exec(df)
    plot_code.airline_delay_comparison.exec(df)

if __name__ == "__main__":
    main()