#!/usr/bin/env python
import sqlite3
from bs4 import BeautifulSoup

from macshared import insert_example_data

if __name__ == "__main__":
	print("Running MAC Monitor")
	insert_example_data()
	# scrape router page for MAC list
	# compare against list of known MACs
	# if new MACs are connected
	#     send email with notification
	# update database with data
