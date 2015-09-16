# Shared resources for MAC Manage
import sqlite3
import time

DATABASE_NAME = "macmonitor.db"
FILE_PATH = "C:/Users/MyUsername/Desktop/"
NETWORK_SSID = "MyNetworkSSID"

def create_notification(new_conns):
	filename = "NEW_CONNECTIONS_" + str(time.time()) + ".txt"
	message = "New connections detected on %s:\n" % NETWORK_SSID
	for (mac, ip) in new_conns:
		message += "MAC: %s, IP: %s\n" % (mac, ip)
	with open(FILE_PATH + filename, 'w') as notif:
		notif.write(message)

def insert_example_data():
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute('''
		INSERT INTO devices(mac)
		VALUES ("foo")
		''')
	c.execute('''
		INSERT INTO connections(device, start_date, latest_date, ip)
		VALUES (1, 123, 456, "bar")
		''')
	conn.commit()
	conn.close()

def insert_example_data_closed():
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute('''
		INSERT INTO devices(mac)
		VALUES ("foo")
		''')
	c.execute('''
		INSERT INTO connections(device, start_date, latest_date, ip, open)
		VALUES (1, 123, 456, "bar", 0)
		''')
	conn.commit()
	conn.close()