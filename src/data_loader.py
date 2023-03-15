__author__ = "Evan Chase, Connor Heaton"

import datetime as dt
import pandas
import math
import json
import random
import time, os
import multiprocessing as mp
from threading import Thread, current_thread
from DataGnome import DataGnome
from queue import Queue
from threading import Thread
import pybaseball as pb
import sqlite3 as sql
from SQLGnome import SQLGnome

START_DT = "2021-04-07"
END_DT = "2022-04-11"
DB_PATH = "database/mlb_data.db"
CACHE = False

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


def data_loader(start_dt, end_dt, gn_count, cache=CACHE):
    """Pulls data from statcast using DataGnomes and
    pushes to SQLite database

    Args:
        start_dt (str): start date
        end_dt (str): end date
        gn_count (int): number of data gnomes
    """

    stop_term = '<END>'
    start_dt = dt.datetime.strptime(start_dt, "%Y-%m-%d")
    end_dt = dt.datetime.strptime(end_dt, "%Y-%m-%d")
    dates = construct_dates(start_dt, end_dt)
    gn_chunk = math.floor(len(dates) / gn_count)
    gn_dates = [dates[x : x + gn_chunk] for x in range(0, len(dates), gn_chunk)]
    print(gn_dates)

    q = Queue()
    sqlgnome = SQLGnome(q, DB_PATH, stop_term, gn_count)
    sqlgnome.connect_db()

    f = open("utils/gnome_names.json")
    gn_names = random.sample(json.load(f), gn_count)
    datagnomes = [
        DataGnome(q, stop_term, gn_dates[gn_id], gn_names[gn_id], gn_id)
        for gn_id in range(gn_count)
    ]        

    if gn_count < len(gn_dates):
        datagnomes[-1].dates = datagnomes[-1].dates + gn_dates[-1]

    print("Data gnomes have been initialized.")

    if cache:
        pb.cache.enable()

    print("Starting statcast threads...")
    gn_process = [Thread(target=gn.pull_statcast, args=()) for gn in datagnomes]

    for p in gn_process:
        p.start()

    time.sleep(5)
    sqlgnome.insert_items_from_q()


if __name__ == "__main__":
    data_loader(start_dt=START_DT, end_dt=END_DT, gn_count=3)
