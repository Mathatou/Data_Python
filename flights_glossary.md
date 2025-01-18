# Flights_Glossary

---

Glossaire de **Flights.csv**

| **Nom du paramètre** | **Description** |
| --- | --- |
| Year | L'année où le vol a eu lieu. |
| Quarter | Le trimestre de l'année (1 = janvier-mars, 2 = avril-juin, etc.). |
| Month | Le mois de l'année (1 = janvier, 2 = février, etc.). |
| DayofMonth | Le jour du mois (1 à 31). |
| DayOfWeek | Le jour de la semaine (1 = lundi, 2 = mardi, etc.). |
| FlightDate | La date complète du vol (format YYYY-MM-DD). |
| Reporting_Airline | Le nom de la compagnie aérienne rapportant les données. |
| DOT_ID_Reporting_Airline | Identifiant unique attribué par le Département des Transports (DOT) pour la compagnie aérienne. |
| IATA_CODE_Reporting_Airline | Code IATA de la compagnie aérienne (ex. : AA pour American Airlines). |
| Tail_Number | Numéro de queue de l'avion (identification de l'appareil). |
| Flight_Number_Reporting_Airline | Numéro de vol rapporté par la compagnie aérienne. |
| OriginAirportID | Identifiant unique de l'aéroport d'origine (attribué par le DOT). |
| OriginAirportSeqID | Identifiant séquentiel unique de l'aéroport d'origine. |
| OriginCityMarketID | Identifiant unique pour la ville associée à l'aéroport d'origine. |
| Origin | Code IATA de l'aéroport d'origine (ex. : JFK pour New York John F. Kennedy). |
| OriginCityName | Nom de la ville associée à l'aéroport d'origine. |
| OriginState | Code de l'état de l'aéroport d'origine (ex. : NY pour New York). |
| OriginStateFips | Code FIPS (Federal Information Processing Standard) de l'état d'origine. |
| OriginWac | Code WAC (World Area Code) de l'aéroport d'origine. |
| DestAirportID | Identifiant unique de l'aéroport de destination. |
| DestAirportSeqID | Identifiant séquentiel unique de l'aéroport de destination. |
| DestCityMarketID | Identifiant unique pour la ville associée à l'aéroport de destination. |
| Dest | Code IATA de l'aéroport de destination. |
| DestCityName | Nom de la ville associée à l'aéroport de destination. |
| DestState | Code de l'état de l'aéroport de destination. |
| DestStateFips | Code FIPS de l'état de destination. |
| DestWac | Code WAC de l'aéroport de destination. |
| CRSDepTime | Heure de départ prévue (au format HHMM). |
| DepTime | Heure réelle de départ (au format HHMM). |
| DepDelay | Retard au départ (en minutes). |
| DepDelayMinutes | Retard au départ (valeur absolue, uniquement si retard > 0). |
| DepDel15 | Indique si le retard au départ dépasse 15 minutes (1 = Oui, 0 = Non). |
| DepartureDelayGroups | Catégorie de retard au départ, par tranches de 15 minutes (négatif = avance). |
| DepTimeBlk | Intervalle de temps pour le départ (ex. : "0700-0759"). |
| TaxiOut | Temps de roulage après départ (en minutes). |
| WheelsOff | Heure où l'avion a décollé (au format HHMM). |
| WheelsOn | Heure où l'avion a atterri (au format HHMM). |
| TaxiIn | Temps de roulage après l'atterrissage (en minutes). |
| CRSArrTime | Heure d'arrivée prévue (au format HHMM). |
| ArrTime | Heure réelle d'arrivée (au format HHMM). |
| ArrDelay | Retard à l'arrivée (en minutes). |
| ArrDelayMinutes | Retard à l'arrivée (valeur absolue, uniquement si retard > 0). |
| ArrDel15 | Indique si le retard à l'arrivée dépasse 15 minutes (1 = Oui, 0 = Non). |
| ArrivalDelayGroups | Catégorie de retard à l'arrivée, par tranches de 15 minutes (négatif = avance). |
| ArrTimeBlk | Intervalle de temps pour l'arrivée (ex. : "0700-0759"). |
| Cancelled | Indique si le vol a été annulé (1 = Oui, 0 = Non). |
| CancellationCode | Raison de l'annulation (A = Transporteur, B = Météo, C = NAS, D = Sécurité). |
| Diverted | Indique si le vol a été dérouté (1 = Oui, 0 = Non). |
| CRSElapsedTime | Temps de vol prévu (en minutes). |
| ActualElapsedTime | Temps de vol réel (en minutes). |
| AirTime | Temps passé en vol (en minutes). |
| Flights | Nombre de segments de vol (généralement 1). |
| Distance | Distance entre l'origine et la destination (en miles). |
| DistanceGroup | Groupe de distance (1 = 1-250 miles, 2 = 251-500 miles, etc.). |
| CarrierDelay | Retard dû au transporteur (en minutes). |
| WeatherDelay | Retard dû aux conditions météorologiques (en minutes). |
| NASDelay | Retard dû au système national de l'espace aérien (en minutes). |
| SecurityDelay | Retard dû aux mesures de sécurité (en minutes). |
| LateAircraftDelay | Retard dû à l'arrivée tardive d'un avion précédent (en minutes). |
| FirstDepTime | Heure de départ initiale en cas de plusieurs départs (au format HHMM). |
| TotalAddGTime | Temps additionnel au sol total (en minutes). |
| LongestAddGTime | Temps additionnel au sol le plus long (en minutes). |