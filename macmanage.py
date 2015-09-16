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
			 mac TEXT,
			 description TEXT DEFAULT NULL)
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
	print("Inner join on device ID")
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute('''
		SELECT mac, start_date, latest_date, ip, open, description
		FROM devices, connections
		WHERE devices.devid = connections.device
		ORDER BY connections.latest_date DESC
		''')
	data = c.fetchall()
	print(tabulate(data, ["MAC", "Start Date", "Latest Date", "IP", "Open", "Description"], tablefmt="psql"))
	conn.close()

def open_connections():
	print("Open Connections:")
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	data = []
	for row in c.execute('''
		SELECT d.mac, c.ip, c.start_date, d.description
		FROM devices d, connections c
		WHERE c.device = d.devid
		AND c.open = 1
		ORDER BY c.ip
		'''):
		timedelta = datetime.now() - datetime.fromtimestamp(row[2])
		data.append([row[0], row[1], timedelta, row[3]])
	print(tabulate(data, ["MAC", "IP", "Connection Time", "Description"], tablefmt="psql"))
	conn.close()

def edit_description():
	print("Choose a device to edit description:")
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute('''
		SELECT devid, mac, description FROM devices
		''')
	macs = c.fetchall()
	print(tabulate(macs, ["ID", "MAC", "Description"], tablefmt="psql"))
	devid = input("Enter ID or press 'q' to quit: ")
	if devid is 'q':
		return
	else:
		desc = input("Enter description for ID %d: " % int(devid))
		c.execute('''
			UPDATE devices
			SET description = ?
			WHERE devid = ?
			''', (desc, int(devid),))
	conn.commit()
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
	parser.add_argument('-e', '--edit-desc', action='store_true',
		help="Edit the description of a device")
	args = parser.parse_args()

	if args.create_db:
		delete_database()
		create_database()

	if args.dump:
		dump_database()

	if args.open_conns:
		open_connections()

	if args.edit_desc:
		edit_description()

	if not any(vars(args).values()): # No arguments passed
		parser.parse_args('-h'.split())

	# provide options to
	#   - Print statistics
