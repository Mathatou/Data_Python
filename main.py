import pandas as pd

import plot_code.histogram_nb_flights_nb_minutes

def main():
    df = pd.read_csv("./csv/flights.csv", encoding='latin1')
    plot_code.histogram_nb_flights_nb_minutes.exec(df)

if __name__ == "__main__":
    main()