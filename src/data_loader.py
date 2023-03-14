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
import SQLGnome

START_DT = "2022-04-07"
END_DT = "2022-05-15"
DB_PATH = "database/mlb_data.db"


def construct_dates(start_dt, end_dt):
    """Generates list of dates for pulling data

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


def data_loader(start_dt, end_dt, gn_count):
    """Pulls data from statcast using DataGnomes and
    pushes to SQLite database

    Args:
        start_dt (str): start date
        end_dt (str): end date
        gn_count (int): number of data gnomes
    """

    start_dt = dt.datetime.strptime(start_dt, "%Y-%m-%d")
    end_dt = dt.datetime.strptime(end_dt, "%Y-%m-%d")
    dates = construct_dates(start_dt, end_dt)
    gn_chunk = math.floor(len(dates) / gn_count)
    gn_ranges = [dates[x : x + gn_chunk] for x in range(0, len(dates), gn_chunk)]
    
    q = Queue()

    f = open("utils/gnome_names.json")
    gn_names = random.sample(json.load(f), gn_count)
    datagnomes = [
        DataGnome(q, gn_ranges[gn_id], gn_names[gn_id], gn_id)
        for gn_id in range(gn_count)
    ]
    if gn_count < len(gn_ranges):
        datagnomes[-1].dates = datagnomes[-1].dates + gn_ranges[-1]


    sqlgnome = SQLGnome(q, DB_PATH)
    sqlgnome.connect_db()

    pb.cache.enable()
    for gn in datagnomes:
        mp.Process(target=gn.pull_statcast, args=()).start()

    sqlgnome.insert_items()


if __name__ == "__main__":
    data_loader(start_dt=START_DT, end_dt=END_DT, gn_count=3)
