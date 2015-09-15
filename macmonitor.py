#!/usr/bin/env python
import sqlite3
from bs4 import BeautifulSoup

if __name__ == "__main__":
	print("Running MAC Monitor")
	# scrape router page for MAC list
	# compare against list of known MACs
	# if new MACs are connected
	#     send email with notification
	# update database with data
