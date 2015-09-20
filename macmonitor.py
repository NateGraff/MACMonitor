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
import subprocess
import re

from macshared import DATABASE_NAME, ROUTER_IP, create_notification

def get_open_connection(mac, ip):
	with sqlite3.connect(DATABASE_NAME) as conn:
		c = conn.cursor()
		c.execute('''
			SELECT connid FROM connections
			INNER JOIN devices on connections.device = devices.devid
			WHERE connections.open = 1
			AND connections.ip = ?
			AND devices.mac = ?
			''', (ip, mac,))
		row = c.fetchone()

	if row:
		return row[0]
	else:
		return None

def update_latest_date(connid):
	with sqlite3.connect(DATABASE_NAME) as conn:
		c = conn.cursor()
		c.execute("""
			UPDATE connections
			SET latest_date =
				(SELECT strftime('%s', 'now'))
			WHERE connid = ?
			""", (str(connid),))
		conn.commit()

def insert_new_connection(mac, ip):
	with sqlite3.connect(DATABASE_NAME) as conn:
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

def close_missing_connections(macs):
	def param_list(length):
		if length is 0:
			return "()"
		else:
			return "(" + ("?," * (length-1)) + "?)"

	with sqlite3.connect(DATABASE_NAME) as conn:
		c = conn.cursor()
		c.execute("""
			UPDATE connections
			SET open = 0
			WHERE device IN
				(SELECT devid from devices
				 WHERE mac NOT IN """ + param_list(len(macs)) +")", tuple(macs))
		conn.commit()

def get_devid(mac):
	with sqlite3.connect(DATABASE_NAME) as conn:
		c = conn.cursor()
		c.execute("""
			SELECT devid from devices
			WHERE mac = ?
			""", (mac,))
		row = c.fetchone()

	if row:
		return row[0]
	else:
		return None

def insert_new_device(mac, desc):
	with sqlite3.connect(DATABASE_NAME) as conn:
		c = conn.cursor()
		c.execute("""
			INSERT INTO devices(mac, description)
			VALUES (?,?)
			""", (mac, desc,))
		conn.commit()

def scan_network():
	nmap_output = subprocess.check_output(["nmap", "-n", "-sP", "%s/24" % ROUTER_IP]).decode("utf-8")
	
	host_pattern = r"Nmap scan report for (\d{3}\.\d{3}\.\d+?\.\d+).*?MAC Address: (.{17}) \((.*?)\)"
	matcher = re.compile(host_pattern, re.DOTALL)
	data = matcher.findall(nmap_output)

	return data


if __name__ == "__main__":
	print("Running MAC Monitor\n")

	data = scan_network()

	new_devices = []
	macs = []

	for (ip, mac, desc) in data:
		macs.append(mac)
		if get_devid(mac):
			if get_open_connection(mac, ip):
				update_latest_date(get_open_connection(mac, ip))
			else:
				insert_new_connection(mac, ip)
		else:
			new_devices.append((mac, ip, desc))
			insert_new_device(mac, desc)
			insert_new_connection(mac, ip)

	close_missing_connections(macs)

	if new_devices:
		create_notification(new_devices)
