# MAC Monitor
MAC Monitor is a tool for high-level tracking of hosts on your network.
I created it because I had a free couple of days, a desire to do something
with SQL, my first home LAN exclusively under my control, and a hint of
paranoia that other jerks might want to hog my internet connection.

Use MAC Monitor at your own risk and only on networks that you're allowed to
futz with.

## Requirements
### Python
* Python >= 3.2
* sqlite3
* tabulate
* argparse

### System Tools
* nmap


## Installation
1. Edit `FILE_PATH`, `DATABASE_NAME`, `NETWORK_SSID`, `ROUTER_IP` in macshared.py
2. Create the database with `python macmanage.py -c`
3. Set up `python macmonitor.py` as scheduled task or cronjob

Copyright (c) 2015, Nathaniel Graff. All rights reserved.