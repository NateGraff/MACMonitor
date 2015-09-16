#!/usr/bin/env python
import sqlite3
import os

from macshared import DATABASE_NAME, insert_example_data

def create_database():
	print("Creating MAC Monitor Sqlite3 Database")

	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute('PRAGMA foreign_keys = ON')
	c.execute('''
		CREATE TABLE devices
			(id INTEGER PRIMARY KEY,
			 mac TEXT)
		''')
	c.execute('''
		CREATE TABLE connections
			(device INTEGER,
			 start_date INTEGER,
			 latest_date INTEGER,
			 ip TEXT,
			 open INTEGER DEFAULT 1,
			 FOREIGN KEY(device) REFERENCES devices(id))
		''')
	conn.close()

def delete_database():
	print("Deleting MAC Monitor Sqlite3 Database")
	os.remove(DATABASE_NAME)

def dump_database():
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute('''
		SELECT mac, start_date, latest_date, ip, open
		FROM devices, connections
		WHERE devices.id = connections.device
		''')
	print(c.fetchall())
	conn.close()

if __name__ == "__main__":
	print("Running MAC Manage")
	delete_database()
	create_database()
	insert_example_data()
	dump_database()
	# provide options to
	#   - Print statistics
	#   - clean/initialize database
