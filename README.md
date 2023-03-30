# mlb-sim
### A simulator for predicting game and season results

MLB sim is a pet project simulator for predicting game and season results of the MLB. The end goal is a complete sim environment where users can input custom lineups and game situations. The sim uses trained models to make predictions on the outcomes.

### Usage
### Data
The data is pulled from a variety of sources using [pybaseball](https://github.com/jldbc/pybaseball) and pushed to a SQLite3 database. The heaviest of tables is statcast, which details pitch by pitch data with advanced metrics such as spin rate, barrell velocity, and launch angle. Statcast was introduced to all 30 mlb stadiums in 2015 and can provide better insight than traditional derivative sabermetric values. Additionally, aggregated pitching and batter data over given time periods are pulled from statcast. The Chadwick register provides unique player ids for easy player lookup.

### Models
### Analysis
