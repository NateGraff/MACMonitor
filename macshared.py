# Shared resources for MAC Manage
import sqlite3
from datetime import datetime

DATABASE_NAME = "macmonitor.db"
FILE_PATH = "C:/Users/MyUsername/Desktop/"
NETWORK_SSID = "MyNetworkSSID"

def create_notification(new_conns):
	filename = "NEW_CONNECTIONS.txt"
	message = "New connections detected on %s:\n" % NETWORK_SSID
	for (mac, ip) in new_conns:
		start_date = get_connection_time(mac, ip)
		message += "MAC: %s, IP: %s, Joined network: %s\n" % (mac, ip, start_date)
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
