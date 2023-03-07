import mysqgl.connector as sql

def create_sql_server(connection, query):
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		print("SQL Database created successfully")
	except Error as err:
		print(f"SQL Database creation failed! '{err}'")