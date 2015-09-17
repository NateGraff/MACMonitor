#!/usr/bin/env python
#
# Copyright (c) 2015, Nathaniel Graff
# All rights reserved.
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sqlite3
import os
import argparse
from datetime import datetime
from tabulate import tabulate

from macshared import DATABASE_NAME

def create_database():
	print("Creating MAC Monitor Sqlite3 Database")

	with sqlite3.connect(DATABASE_NAME) as conn:
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
				 FOREIGN KEY(device) REFERENCES devices(devid) ON DELETE CASCADE)
			''')
		conn.commit()

def delete_database():
	print("Deleting MAC Monitor Sqlite3 Database")
	os.remove(DATABASE_NAME)

def dump_database():
	print("MAC Monitor Database Dump:")
	print("Inner join on device ID")
	with sqlite3.connect(DATABASE_NAME) as conn:
		c = conn.cursor()
		c.execute('''
			SELECT mac, start_date, latest_date, ip, open, description
			FROM devices, connections
			WHERE devices.devid = connections.device
			ORDER BY connections.latest_date DESC
			''')
		data = c.fetchall()
		print(tabulate(data, ["MAC", "Start Date", "Latest Date", "IP", "Open", "Description"], tablefmt="psql"))

def open_connections():
	print("Open Connections:")
	with sqlite3.connect(DATABASE_NAME) as conn:
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

def edit_description():
	print("Choose a device to edit description:")
	with sqlite3.connect(DATABASE_NAME) as conn:
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

def forget_device():
	print("Choose a device to forget:")
	with sqlite3.connect(DATABASE_NAME) as conn:
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
			c.execute('''
				DELETE FROM devices
				WHERE devid = ?
				''', (int(devid),))
		conn.commit()

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
	parser.add_argument('-f', '--forget-device', action='store_true',
		help="Forget a device and its connections")
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

	if args.forget_device:
		forget_device()

	if not any(vars(args).values()): # No arguments passed
		parser.parse_args('-h'.split())

	# provide options to
	#   - Print statistics
