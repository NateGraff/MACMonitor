# Shared resources for MAC Manage
import sqlite3

DATABASE_NAME = "macmonitor.db"

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
