#!/usr/bin/env python
import sqlite3
import os
import argparse
from datetime import datetime
from tabulate import tabulate

from macshared import DATABASE_NAME

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
	conn.commit()
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
		ORDER BY connections.latest_date DESC
		''')
	data = c.fetchall()
	print(tabulate(data, ["MAC", "Start Date", "Latest Date", "IP", "Open"], tablefmt="psql"))
	conn.close()

def open_connections():
	print("Open Connections:")
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	data = []
	for row in c.execute('''
		SELECT d.mac, c.ip, c.start_date
		FROM devices d, connections c
		WHERE c.device = d.devid
		AND c.open = 1
		ORDER BY c.ip
		'''):
		timedelta = datetime.now() - datetime.fromtimestamp(row[2])
		data.append([row[0], row[1], timedelta])
	print(tabulate(data, ["MAC", "IP", "Connection Time"], tablefmt="psql"))
	conn.close()

if __name__ == "__main__":
	print("Running MAC Manage\n")

	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--create-db', action='store_true',
		help="Create a blank MAC Monitor database")
	parser.add_argument('-d', '--dump', action='store_true',
		help="Dump the contents of the MAC Monitor database")
	parser.add_argument('-o', '--open-conns', action='store_true',
		help="List currently open connections")
	args = parser.parse_args()

	if args.create_db:
		delete_database()
		create_database()

	if args.dump:
		dump_database()

	if args.open_conns:
		open_connections()

	if not (args.create_db or args.dump or args.open_conns):
		parser.parse_args('-h'.split())

	# provide options to
	#   - Print statistics
