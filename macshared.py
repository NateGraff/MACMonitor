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
