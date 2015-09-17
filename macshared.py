# Shared resources for MAC Manage
import sqlite3
from datetime import datetime
from tabulate import tabulate

FILE_PATH = "C:/Users/MyUsername/Desktop/"
DATABASE_NAME = "C:/Path/To/macmonitor.db"
NETWORK_SSID = "MyNetworkSSID"

def create_notification(new_conns):
	filename = "NEW_CONNECTIONS.txt"
	message = "%s -- New connections detected on %s:\n" % (datetime.now(), NETWORK_SSID)

	message += tabulate(new_conns, ["MAC", "IP", "Description"])
	message += "\n\n"

	with open(FILE_PATH + filename, 'a') as notif:
		notif.write(message)

def get_connection_time(mac, ip):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute('''
		SELECT c.start_date
		FROM devices d, connections c
		WHERE d.devid = c.device
		AND d.mac = ?
		AND c.ip = ?
		AND c.open = 1
		''', (mac, ip,))
	row = c.fetchone()
	conn.close()
	return str(datetime.fromtimestamp(row[0]))
