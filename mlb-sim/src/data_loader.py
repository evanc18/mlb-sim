__author__ = "Evan Chase"

import datetime as dt
import pandas
import math
import json
import random
import time, os
import multiprocessing as mp
import argparse
from threading import Thread, current_thread
from DataGnome import DataGnome
from queue import Queue
from threading import Thread
import pybaseball as pb
import sqlite3 as sql
from SQLGnome import SQLGnome

START_DT = "2021-03-25"
END_DT = "2021-12-01"
DB_PATH = "database/mlb_data.db"
CACHE = True


def construct_dates(start_dt, end_dt):
    """Generates daily list of dates for pulling data

    Args:
            start_dt (str): start date
            end_dt (str): end date

    Returns:
            List: list of dates
    """
    return (
        pandas.date_range(start_dt, end_dt - dt.timedelta(days=1), freq="d")
        .strftime("%Y-%m-%d")
        .tolist()
    )


def data_loader(args):
    """Receives outbound DataGnome items for chosen tables and pushes out to SQLWorker

    Args:
        args: command line args of chosen tables and dates
    """

    DB_PATH = args.db
    start_dt = dt.datetime.strptime(args.start_dt, "%Y-%m-%d")
    end_dt = dt.datetime.strptime(args.end_dt, "%Y-%m-%d")
    gn_count = args.gn_count

    dates = construct_dates(start_dt, end_dt)
    gn_chunk = math.floor(len(dates) / gn_count)
    gn_dates = [
        dates[x : x + gn_chunk] for x in range(0, len(dates), gn_chunk)
    ]
    print(gn_dates)
    
    q = Queue()

    f = open("utils/gnome_names.json")
    gn_names = random.sample(json.load(f), gn_count)
    datagnomes = [
        DataGnome(q, gn_dates[gn_id], gn_names[gn_id], gn_id)
        for gn_id in range(gn_count)
    ]

    if gn_count < len(gn_dates):
        datagnomes[-1].dates = datagnomes[-1].dates + gn_dates[-1]

    print("Data gnomes have been initialized.")

    if args.cache:
        pb.cache.enable()

    working = True
    sqlgnome = SQLGnome(q, DB_PATH, gn_count)
    sqlgnome.connect_db()

    if args.statcast:
        print("Starting statcast threads...")
        while working:
            gn_process = [
                Thread(target=gn.pull_statcast, args=())
                for gn in datagnomes
            ]
            for p in gn_process:
                p.start()
            time.sleep(3)
            working = sqlgnome.insert_items_from_q("statcast")
        working = True

    #Aggregate and small tables pull only use one gnome
    sqlgnome.reset_stop_lim(1)
    if args.pitching_stats_range:
        print("Starting pitching stats range thread...")
        while working:
            gn_process = Thread(target=datagnomes[0].pull_pitching_stats_range, args=())
            gn_process.start()
            time.sleep(3)
            working = sqlgnome.insert_items_from_q("pitching_stats_range")
        working = True
    
    sqlgnome.reset_stop_lim(1)
    if args.batting_stats_range:
        print("Starting batting stats range thread...")
        while working:
            gn_process = Thread(target=datagnomes[0].pull_batting_stats_range, args=())
            gn_process.start()
            time.sleep(3)
            working = sqlgnome.insert_items_from_q("batting_stats_range")
    
    sqlgnome.reset_stop_lim(1)
    if args.chadwick:
        print("Starting chadwick thread...")
        while working:
            gn_process = Thread(target=datagnomes[0].pull_chadwick, args=())
            gn_process.start()
            time.sleep(3)
            working = sqlgnome.insert_items_from_q("chadwick")

    if args.live_schedule:
        datagnomes[0].pull_live_schedule()
    
    if args.live_game:
        datagnomes[0].pull_live_game(args.live_game)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pull various mlb data")
    parser.add_argument(
        "--db",
        metavar="path",
        default=DB_PATH,
        required=False,
        type=str,
        help='path to db where tables will be created',
    )
    parser.add_argument(
        "--start_dt",
        metavar="path",
        default=START_DT,
        required=False,
        type=str,
        help='the start date "YYYY-MM-DD"',
    )
    parser.add_argument(
        "--end_dt",
        metavar="path",
        default=END_DT,
        required=False,
        type=str,
        help='the end date "YYYY-MM-DD"',
    )
    parser.add_argument(
        "--gn_count",
        metavar="path",
        default=3,
        required=False,
        type=int,
        help="number of data gnomes",
    )
    parser.add_argument(
        "--cache",
        metavar="path",
        default=True,
        required=False,
        help="enable pybaseball caching",
    )
    parser.add_argument(
        "--statcast",
        metavar="path",
        default=False,
        required=False,
        help="statcast pitch by pitch",
    )
    parser.add_argument(
        "--pitching_stats_range",
        metavar="path",
        default=False,
        required=False,
        help="aggregate pitching stats over given time period",
    )
    parser.add_argument(
        "--batting_stats_range",
        metavar="path",
        default=False,
        required=False,
        help="aggregate batting stats over given time period",
    )
    parser.add_argument(
        "--chadwick",
        metavar="path",
        default=False,
        required=False,
        help="chadwick register people info",
    )
    parser.add_argument(
        "--live_schedule",
        metavar="path",
        default=False,
        required=False,
        help="today's live lineups and games",
    )
    parser.add_argument(
        "--live_game",
        metavar="path",
        default=0,
        required=False,
        help="live game data",
    )
    args = parser.parse_args()
    data_loader(args)
