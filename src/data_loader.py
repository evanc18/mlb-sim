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
	return pandas.date_range(start_dt, end_dt-dt.timedelta(days=1), freq='d').strftime("%Y-%m-%d").tolist()

def data_loader(start_dt, end_dt, gn_count):

	start_dt = dt.datetime.strptime(start_dt, "%Y-%m-%d")
	end_dt = dt.datetime.strptime(end_dt, "%Y-%m-%d")

	dates = construct_dates(start_dt, end_dt)
	gn_chunk = math.floor(len(dates)/gn_count)
	gn_ranges = [dates[x:x+gn_chunk] for x in range(0, len(dates), gn_chunk)] 

	f = open('gnome_names.json')
	names = random.sample(json.load(f), gn_count)
	datagnomes = [DataGnome([], gn_ranges[gn_id], names[gn_id], gn_id) for gn_id in range(gn_count)]
	if gn_count<len(gn_ranges):
		datagnomes[-1].dates = datagnomes[-1].dates + gn_ranges[-1]

	sqlgnome = SQLGnome([], Queue(), DB_PATH)
	sqlgnome.connect_db()
	
	
	pb.cache.enable()
	for gn in datagnomes:
		mp.Process(target=gn.pull_statcast, args=()).start()

	



	





if __name__=="__main__":
	data_loader(start_dt=START_DT, end_dt=END_DT, gn_count=3)

