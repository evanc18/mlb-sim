__author__ = 'Evan Chase'

import pybaseball as pb
import itertools
import contextlib


class DataGnome:
	"""The summary line for a class docstring should fit on one line.

	If the class has public attributes, they may be documented here
	in an ``Attributes`` section and follow the same formatting as a
	function's ``Args`` section. Alternatively, attributes may be documented
	inline with the attribute's declaration (see __init__ method below).

	Properties created with the ``@property`` decorator should be documented
	in the property's getter method.

	Attributes:
	attr1 (str): Description of `attr1`.
	attr2 (:obj:`int`, optional): Description of `attr2`.
	"""

	def __init__(self, args, dates, name, gn_id):
		self.args = args
		self.dates = dates
		self.name = name
		self.gn_id = gn_id
		self.lifespan = len(dates)
		self.max_chunk = 10

		print("Data gnome " + name + " has been initialized")
		
	def pull_statcast(self):
		"""Query data from statcast for given date range

		"""
		max_chunk = 10
		dates_chunked = [self.dates[x:x+max_chunk] for x in range(0, len(self.dates), max_chunk)] 
		for chunk in dates_chunked:
			print(self.name + " pulling " + str(len(chunk)) + " dates...\n")
			data = pb.statcast(start_dt=chunk[0],
				end_dt=chunk[-1],
				verbose=False)
			print(self.name + " pulled " + str(len(chunk)) + " dates!\n")