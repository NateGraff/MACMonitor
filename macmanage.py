#!/usr/bin/env python
import sqlite3
import os
import argparse

from macshared import DATABASE_NAME, insert_example_data

def create_database():
	print("Creating MAC Monitor Sqlite3 Database")

	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute('PRAGMA foreign_keys = ON')
	c.execute('''
		CREATE TABLE devices
			(devid INTEGER PRIMARY KEY,
			 mac TEXT)
		''')
	c.execute('''
		CREATE TABLE connections
			(connid INTEGER PRIMARY KEY,
			 device INTEGER,
			 start_date INTEGER,
			 latest_date INTEGER,
			 ip TEXT,
			 open INTEGER DEFAULT 1,
			 FOREIGN KEY(device) REFERENCES devices(devid))
		''')
	conn.close()

def delete_database():
	print("Deleting MAC Monitor Sqlite3 Database")
	os.remove(DATABASE_NAME)

def dump_database():
	print("MAC Monitor Database Dump:")
	print("Inner join on MAC id")
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute('''
		SELECT mac, start_date, latest_date, ip, open
		FROM devices, connections
		WHERE devices.devid = connections.device
		''')
	print(c.fetchall())
	conn.close()

if __name__ == "__main__":
	print("Running MAC Manage\n")

	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--create-db', action='store_true',
		help="Create a blank MAC Monitor database")
	parser.add_argument('-d', '--dump', action='store_true',
		help="Dump the contents of the MAC Monitor database")
	args = parser.parse_args()

	if args.create_db:
		delete_database()
		create_database()

	if args.dump:
		dump_database()

	if not (args.create_db or args.dump):
		parser.parse_args('-h'.split())

	# provide options to
	#   - Print statistics
