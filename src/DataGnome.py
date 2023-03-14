__author__ = "Evan Chase"

import pybaseball as pb
import itertools
import contextlib


def check_nan_value(x):
    nan = False
    try:
        nan = math.isnan(x)
    except Exception as ex:
        nan = type(x) == NAType

    return nan


class DataGnome:
    def __init__(self, q_out, dates, name, id, max_chunk=10):
        self.q_out = q_out
        self.dates = dates
        self.name = name
        self.id = id
        self.max_chunk = max_chunk
        self.lifespan = len(dates)
        
        print("Data gnome " + name + " has been initialized")

    def pull_statcast(self):
        """Query data from statcast for given date range"""
        max_chunk = 10
        dates_chunked = [
            self.dates[x : x + max_chunk] for x in range(0, len(self.dates), max_chunk)
        ]
        for chunk in dates_chunked:
            print(self.name + " pulling " + str(len(chunk)) + " dates...")
            data = pb.statcast(start_dt=chunk[0], end_dt=chunk[-1], verbose=False)
            for item_data in data.values.toList():
                item_data[1] = str(item_data[1].strftime("%Y-%m-%d"))
                item_data = [None if check_nan_value(id_) else id_ for id_ in item_data]
                item_data = item_data[:-3]
                self.out_q.put(item_data)
                self.n_items_processed += 1

            print(self.name + " pulled " + str(len(chunk)) + " dates!")

    #TODO pull_statcast_player
    #id = pb.playerid_lookup('kershaw', 'clayton')
    #pb.statcast_pitcher(start_dt, end_dt, id)

    #TODO pull_statcast_pitching_stats
    #pb.pitching_stats_range(start_dt, end_dt)

    #TODO pull_statcast_schedule_and_record
    #pb.schedule_and_record(year, 'NYY')

    #TODO pull_statcast_standings
    #pb.standings(year) -> list of dataframes of divisions

    #TODO pull_mlb_top_prospects
    #pb.top_prospects(teamName=None, playerName=None)

    #TODO pull_lahman

    def cache():
        pb.cache.enable()
