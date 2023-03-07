__author__ = 'Evan Chase'

import pybaseball as pb
import itertools
import contextlib


class SQLGnome:
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

	def __init__(self, q, db_path):
		self.q = q
		self.db_path = db_path
		self.conn = None

	def connect_db(self):
		success = False
		try: 	
			self.conn = sql.connect(self.db_path)
			success = True
		except Error as e:
			print(f"Fatal: SQL Database failed to connect! '{e}'")
			
		return success
		
		
	def create_table(self, q_string):
		success = False
		try:
			c = self.conn.cursor()
			c.execute(q_string)
			success = True
		except Error as e:
			print(f"Error in table creation: '{e}")

		return success

	def insert_items(self):
		self.connect_db

		
		