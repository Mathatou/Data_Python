import folium
import pandas as pd
import geopandas as geopd

airport_df = pd.read_csv("./csv/airports.csv", encoding='latin1')
flight_df = pd.read_csv("./csv/flights.csv", encoding='latin1')

Washington_DC_coordinate = (38.889805, -77.009056)

# Vérifiez que les colonnes nécessaires sont présentes
if not {'latitude_deg', 'longitude_deg', 'name'}.issubset(airport_df.columns):
    raise ValueError("Le fichier CSV doit contenir les colonnes 'latitude_deg', 'longitude_deg', et 'name'.")



us_map = folium.Map(location=Washington_DC_coordinate, tiles='OpenStreetMap', zoom_start=4)
value_counts = airport_df['type'].value_counts()

# Afficher uniquement les valeurs qui apparaissent plus d'une fois
duplicates = value_counts[value_counts > 1]

print("Valeurs dupliquées et leur nombre d'occurrences :")
print(duplicates)

#Trop gros de pointer sur tous les airports logique duuuh

# for _, row in df.iterrows():
#     folium.Marker(
#         location=[row['latitude_deg'], row['longitude_deg']],
#         popup=row['name'],  # Affiche le nom de l'aéroport en popup
#         icon=folium.Icon(color='blue', icon='info-sign')
#     ).add_to(us_map)


us_map.save(outfile='map.html')
