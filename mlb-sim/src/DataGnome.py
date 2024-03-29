__author__ = "Evan Chase"

import pybaseball as pb
import pandas as pd
import itertools
import contextlib
import math
from pandas._libs.missing import NAType
from datetime import date
import time
import statsapi
import json


def check_nan_value(x):
    nan = False
    try:
        nan = math.isnan(x)
    except Exception as ex:
        nan = type(x) == NAType

    return nan


class DataGnome:
    def __init__(self, q_out, dates, name, id, stop_term='<END>', max_chunk=10):
        """Gnome for pulling data and pushing to outbound queue

        Args:
            q_out (Queue): queue for pulling
            stop_term (str): stop indicator 
            dates (List): list of dates range to pull 
            name (str): name identifier
            id (int): id identifier
            max_chunk (int, optional): maximum pull range size. Defaults to 10.
        """
        self.q_out = q_out
        self.stop_term = stop_term
        self.dates = dates
        self.name = name
        self.id = id
        self.max_chunk = max_chunk
        self.dates_chunked = [
            self.dates[x : x + self.max_chunk]
            for x in range(0, len(self.dates), self.max_chunk)
        ]
        self.n_items_processed = 0
        self.n_dates_processed = 0

    def log_progress(self):
        """Prints progress of pull"""
        print("{} pulled {}/{} dates!".format(self.name, self.n_dates_processed, len(self.dates)))

    def pull_statcast(self):
        """Query data from statcast for given date range"""
        pb.cache.enable()
        for chunk in self.dates_chunked:
            # print(self.name + " pulling " + str(len(chunk)) + " dates...")
            data = pb.statcast(
                start_dt=chunk[0], end_dt=chunk[-1], verbose=False
            )
            for item_data in data.values.tolist():
                item_data[1] = str(item_data[1].strftime("%Y-%m-%d"))
                item_data = [
                    None if check_nan_value(id_) else id_ for id_ in item_data
                ]
                item_data = item_data[:-3]
                self.q_out.put(item_data)
                self.n_items_processed += 1
            self.n_dates_processed += len(chunk)
            self.log_progress()
        self.q_out.put(self.stop_term)   

    def pull_pitching_stats_range(self):
        """Pushes league-wide season level aggregate pitching data, one row per player per time range from BaseballReference 
        """
        pb.cache.enable()
        data = pb.pitching_stats_range(
            start_dt=self.dates[0], end_dt=self.dates[-1]
        )
        print(data)
        for item_data in data.values.tolist():
            item_data = [
                None if check_nan_value(mlbID) else mlbID for mlbID in item_data
            ]
            self.q_out.put(item_data)
        self.q_out.put(self.stop_term)

    def pull_batting_stats_range(self):
        """Pushes league-wide season level aggregate batting data, one row per player per time range from BaseballReference 
        """
        pb.cache.enable()
        data = pb.batting_stats_range(
            start_dt=self.dates[0], end_dt=self.dates[-1]
        )
        print(data)
        for item_data in data.values.tolist():
            item_data = [
                None if check_nan_value(mlbID) else mlbID for mlbID in item_data
            ]
            self.q_out.put(item_data)
        self.q_out.put(self.stop_term)

    def pull_chadwick(self, save=True):
        """Pushes the Chadwick register of people info
        """
        data = pb.chadwick_register(save=save)
        for item_data in data.values.tolist():
            item_data = [None if check_nan_value(key_fangraphs) else key_fangraphs for key_fangraphs in item_data]
            self.q_out.put(item_data)
        self.q_out.put(self.stop_term)

##These live data pulls will probably be moved to a different file 
    def pull_live_schedule(self):
        today = date.today()
        sched = statsapi.get("schedule", {"sportId": 1, "startDate": today, "endDate": today,"gameType": "R,F,D,L,W", "fields": "dates, date, games, gamePk, gameType"})
        game_list = pd.DataFrame(sched['dates'][0]['games'])
        gamepks = game_list['gamePk']
        games_df = []

        for gamepk in gamepks:
            game_data = statsapi.get("game", {"gamePk": gamepk})['gameData']
            game = {}
            game["gamePk"] = gamepk
            game["home"] = game_data['teams']['home']['name']
            game['away'] = game_data['teams']['away']['name']
            game['date'] = game_data['datetime']['officialDate']
            game['time'] = game_data['datetime']['time'] + " " + game_data['datetime']['ampm']
            game['park'] = game_data['venue']['name']
            game['park_id'] = game_data['venue']['id']
            game['weather'] = game_data['weather']['condition']
            game['temp'] = game_data['weather']['temp']
            game['wind'] = game_data['weather']['wind']
            game['probable_home'] = game_data['probablePitchers']['home']['fullName']
            game['probable_away'] = game_data['probablePitchers']['away']['fullName']
            games_df.append(game)
        return games_df

    def pull_live_game(self, gamepk):
        game_data = statsapi.get("game", {"gamePk": gamepk})
        game = {}
        game["currentPlay"] = game_data['liveData']['plays']['currentPlay']
        game['allPlays'] = game_data['liveData']['plays']['allPlays']
        game['boxScore'] = game_data['liveData']['boxscore']
        game['decisions'] = game_data['liveData']['decisions']
        return game

    # TODO pull_statcast_player
    # id = pb.playerid_lookup('kershaw', 'clayton')
    # pb.statcast_pitcher(start_dt, end_dt, id)

    # TODO pull_statcast_schedule_and_record
    # pb.schedule_and_record(year, 'NYY')

    # TODO pull_statcast_standings
    # pb.standings(year) -> list of dataframes of divisions

    # TODO pull_mlb_top_prospects
    # pb.top_prospects(teamName=None, playerName=None)

    # TODO pull_lahman


