# mlb-sim
### A simulator for predicting game and season results

MLB sim is a pet project simulator for predicting game and season results of the MLB. The end goal is a complete sim environment where users can input custom lineups and game situations. The sim uses trained models to make predictions on the outcomes.

#TODO Credits and thanks

#Access

### Usage
The sim is run through a Node.js web server, that can be accessed [here](www.gnomebaseball.com). Disclaimer: the data and models provided are for entertainment and analytics purposes only. I am not responsible for any gambling losses informed by usage of the app.

#TODO Run local option

#TODO Credentialing?

#TODO Dashboard

#TODO Sim 

#TODO Doc


### Data
The data is pulled from a variety of sources using [pybaseball](https://github.com/jldbc/pybaseball) and pushed to a SQLite3 database. The heaviest of tables is statcast, which details pitch by pitch data with advanced metrics such as spin rate, barrell velocity, and launch angle. Statcast was introduced to all 30 mlb stadiums in 2015 and can provide better insight than traditional derivative sabermetric values. Additionally, aggregated pitching and batter data over given time periods are pulled from statcast. The Chadwick register provides unique player ids for easy player lookup. Live game data is pulled using [statsapi](https://github.com/toddrob99/MLB-StatsAPI/wiki).

The choices for these data sources, while primarily an exercise in databse management for myself, allow for a great degree of freedom and creativity in analysis. Finding links between seemingly unrelated sources yields unexpected but potentially uselful predections.

### Models

#TODO Basic models

#TODO Advanced models


### Analysis
