#!/usr/bin/env python
import sqlite3
from bs4 import BeautifulSoup

from macshared import DATABASE_NAME, insert_example_data, insert_example_data_closed

def get_open_connection(mac):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute('''
		SELECT connid FROM connections
		INNER JOIN devices on connections.device = devices.devid
		WHERE connections.open = 1
		AND devices.mac = ?
		''', (mac,))
	row = c.fetchone()
	conn.close()

	if row:
		return row[0]
	else:
		return None

def update_latest_date(connid):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute("""
		UPDATE connections
		SET latest_date =
			(SELECT strftime('%s', 'now'))
		WHERE connid = ?
		""", (str(connid),))
	conn.commit()
	conn.close()

def insert_new_connection(mac, ip):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute("""
		UPDATE connections
		SET open = 0
		WHERE device = 
			(SELECT devid from devices
			 WHERE mac = ?)
		""", (mac,))
	c.execute("""
		INSERT INTO connections(device, start_date, latest_date, ip)
		VALUES
		(
			(SELECT devid from devices
			 WHERE mac = ?),
			(SELECT strftime('%s', 'now')),
			(SELECT strftime('%s', 'now')),
			?
		)
		""", (mac, ip,))
	conn.commit()
	conn.close()

def get_devid(mac):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute("""
		SELECT devid from devices
		WHERE mac = ?
		""", (mac,))
	row = c.fetchone()
	conn.close()

	if row:
		return row[0]
	else:
		return None

def insert_new_device(mac):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute("""
		INSERT INTO devices(mac)
		VALUES (?)
		""", (mac,))
	conn.commit()
	conn.close()

if __name__ == "__main__":
	print("Running MAC Monitor\n")

	# TODO: get data from somewhere
	data = [('f8-e0-79-bf-b0-64', '192.168.0.2'),] # list of current hosts

	new_devices = []

	for (mac, ip) in data:
		if get_devid(mac):
			if get_open_connection(mac):
				update_latest_date(get_open_connection(mac))
			else:
				insert_new_connection(mac, ip)
		else:
			new_devices += [(mac, ip,)]
			insert_new_device(mac)
			insert_new_connection(mac, ip)

	# TODO: close connections not listed in data

	if new_devices:
		# TODO: send email with notification
		print("NEW DEVICES DETECTED: " + str(new_devices))
