import sqlite3
import numpy as np
import datetime as dt
conn = sqlite3.connect('Velov.sqlite')
c = conn.cursor()
c.execute("SELECT DISTINCT commune FROM 'station-velov2018'")
r = c.fetchall()
print(r)