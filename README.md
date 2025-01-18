# Rapport

---

# User Guide

Afin de déployer et utiliser notre dashboard sur une autre machine voici ce qu’il faut faire. Avant toute chose il faut avoir cloné le repository, puis en se plaçant dans le dossier courant du projet il faut installer les requirements, lancer le fichier principal “main.py”.

```bash
git clone https://github.com/Mathatou/Data_Python.git
python -m pip install -r requirements.txt 
python main.py
```

Le jeu de données (plus d’informations dans la section suivante) est un extrait d’un fichier plus gros 80Go, nos données ne sont donc pas nécessairement les plus précises. 

Nous avons également un fichier *get_data.py* qui télécharge les données (ce qui pourrait nous permettre d’utiliser le jeu de données global ) puis un fichier *clean_data.py* qui va les nettoyer pour les préparer pour l’utilisation. Cependant, nous avons opté pour une autre méthode, nous avons gardé nos csv compressés et nous appelons notre fichier *extract_csv.py* qui les décompresse pour l’utilisation et l’analyse.

# Data

- **Airlines.csv :** Ce jeu de données représente les différentes compagnies de vols. Ce fichier est composé des nom des transporteurs ainsi qu’un code unique qui leur est attribué à chacun.
- **Airports.csv :** Ce jeu de données contient tous les aéroports, héliports et autres aérodromes présents aux États-Unis. Afin de se concentrer sur les données de vols d’avions, nous avons écartés tous type d’aérodromes n’étant pas un aéroport.
- **Flights.csv :** C’est le jeu de données principal que nous avons utilisé, il regroupe tous les vols aux États-Unis entre 1987 et 2020. De plus, en lien avec le fichier **Airports.csv**, nous avons également retiré tous les vols d’hélicoptères et aéronefs afin de ne garder que les vols d’avions.
    
    Ce faisant, nous avons identifié un problème dans notre jeu de données. Il n’y a aucun avion qui décolle depuis le Maryland. Nous pensons donc que notre jeu de données est erroné, ou que les données de vols du Maryland se situe dans le fichier global. 
    
- **States.csv :** Nous avons écris ce fichier regroupant le nom de chaque états (Alabama), leur code (AL) ainsi que leurs coordonnées géographiques (lat, long) .

# Developper Guide

```mermaid
%% Section 1 : utils
graph TD
    B[utils]
    B --> B1[clean<br>_data.py]
    B --> B2[download.py]
    B --> B3[extract<br>_csv.py]
```

```mermaid
%% Section 2 : map et plot_code
graph TD
    C[map]
    C --> C1[flight<br>_per<br>_state.py]
    C --> C2[geous.geojson]

    D[plot_code]
    D --> D1[airline<br>_performance<br>_comparison.py]
    D --> D2[carrier<br>_market<br>_comparison.py]
    D --> D3[delay<br>_distribution.py]
    D --> D4[delay<br>_duration.py]
    D --> D5[time<br>_distribution<br>_component.py]
```

```mermaid
%% Section 3 : src, csv et data
graph TD
    E[src]
    E --> E1[utils<br>/time.py]

    F[csv]
    F --> F1[airlines.csv]
    F --> F2[airports.csv]
    F --> F3[flights.csv]
    F --> F4[states.csv]

    G[data]
    G --> G1[compressed<br>/airlines.zip]
    G --> G2[compressed<br>/airports.zip]
    G --> G3[compressed<br>/flights.zip]
    G --> G4[compressed<br>/states.zip]
```

Dans chacun des différents fichiers dans le dossier plot_code, il y a une fonction *__init__* qui initialise une instance de la classe, puis une fonction *create_component(self)* qui va créer le graphique ou la carte correspondante. Dans le main, nous avons crée le dashboard et chaque composants sont générés grâce à l’appel de *create_component*.

Afin d’ajouter un plot au dashboard,  il suffit de décrire votre composant dans une classe qui sera  située dans le dossier plot_code. Une fois cela fait, il faut rajouter une ligne dans le dashboard en suivant ce qui a été fait précédemment et de rajouter *MaClasse.create_component()* dans le corps du dashboard comme ceci :

```python
dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Flights Distribution by Time Period"),
                    dbc.CardBody(
                        time_dist.create_component()
                    )
                ], className="mb-4")
            ], width=12, lg=6)
        ])
```

# Rapport d’Analyse

Suite à nos différentes analyses, on a pu arriver à multiples conclusions : 

### Performance des Compagnies Aériennes

- Premièrement, grâce à la première carte et à son graphique circulaire associé, on remarque que **Delta Air Lines Inc.** est la compagnie aérienne américaine la plus empruntée (172 251 vols entre 1987 et 2020)
- Deuxièmement, nous avons un graphique en barres qui donne des indications sur les performances des différentes compagnies aériennes. Le graphique nous renseigne sur le retard moyen ainsi que sur le taux d’annulation de vols. On voit que **Envoy Air** est la compagnie qui annule le plus ses vols et que **JetBlue Airways** est la compagnie ayant en moyenne, le plus de retards.

### Analyse des Retards

- Grâce à l’avant-dernier graphique, on observe que le nombre de retards commence à augmenter progressivement à partir des premières heures du matin (vers 5h-6h).
- Les retards atteignent un **pic en milieu ou fin de journée**, probablement entre 15h et 18h. Cela pourrait être lié à l'effet d'accumulation des retards, où les vols retardés en matinée impactent les vols ultérieurs.
- Les vols programmés très tôt (entre 0h-5h) et tard (22h-23h) présent beaucoup moins de retards. On peut expliquer ceci par un trafic aérien moins encombré.
- Les créneaux horaires les plus chargés en termes de départs (milieu de journée et après-midi) coïncident avec un nombre élevé de retards. Cela pourrait être dû à une saturation des aéroports et des contrôles, ainsi qu'aux effets boule de neige des retards précédents.

### Analyse des Itinéraires

- Sur la première carte, on remarque une concentration élevée sur certains États, les états plus foncés (comme New York ou la Californie) indiquent une fréquence de vols plus élevée. Cela est probablement lié à la densité de population élevée et à la présence de grands hubs aériens (comme New York City et Los Angeles).
- On comprend que les côtes sont très importantes aux États-Unis, elles montrent une plus forte densité de vols comparée au centre du pays. Cela reflète la tendance générale des grandes métropoles et zones côtières à attirer plus de trafic aérien.
- Les États plus clairs (ex. Dakota du Nord, Montana) ont moins de vols en raison de leur faible densité de population et leur faible attractivité touristique ou économique à l'échelle nationale.

# Copyright

Pour ce projet, nous avons utilisé GitHub Copilot, une IA intégrée à nos IDE, comme assistance au développement. Bien que certaines parties du code aient été générées automatiquement, nous avons développé la majorité nous-mêmes.

Par ailleurs, nous avons apporté des modifications au fichier **States.csv** et à la structure du fichier **geous.geojson**.

# Ressources

En suivant ce lien, vous trouverez le glossaire concernant le fichier **Airports.csv,** renseignant sur les différentes données que l’on peut y retrouver.
[Glossaire de airports.csv](airports_glossary.md)

Idem pour celui-ci. Il renseigne sur **Flights.csv.**
[Glossaire de flights.csv](flights_glossary.md)
