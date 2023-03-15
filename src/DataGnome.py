__author__ = "Evan Chase"

import pybaseball as pb
import itertools
import contextlib
import math
from pandas._libs.missing import NAType
import time


def check_nan_value(x):
    nan = False
    try:
        nan = math.isnan(x)
    except Exception as ex:
        nan = type(x) == NAType

    return nan


class DataGnome:
    def __init__(self, q_out, stop_term, dates, name, id, max_chunk=10):
        self.q_out = q_out
        self.stop_term = stop_term
        self.dates = dates
        self.name = name
        self.id = id
        self.max_chunk = max_chunk
        self.n_items_processed = 0
        self.n_dates_processed = 0

    def pull_statcast(self):
        """Query data from statcast for given date range"""
        dates_chunked = [
            self.dates[x : x + self.max_chunk] for x in range(0, len(self.dates), self.max_chunk)
        ]

        for chunk in dates_chunked:
            #print(self.name + " pulling " + str(len(chunk)) + " dates...")
            data = pb.statcast(start_dt=chunk[0], end_dt=chunk[-1], verbose=False)
            for item_data in data.values.tolist():
                item_data[1] = str(item_data[1].strftime("%Y-%m-%d"))
                item_data = [None if check_nan_value(id_) else id_ for id_ in item_data]
                item_data = item_data[:-3]
                self.q_out.put(item_data)
                self.n_items_processed += 1
            self.n_dates_processed += len(chunk)
            print("{} pulled {}/{} dates!".format(self.name, self.n_dates_processed, len(self.dates)))
        self.q_out.put(self.stop_term)
        
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


