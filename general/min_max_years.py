from pprint import pprint
import sqlite3

conn = sqlite3.connect("congress.db")
c = conn.cursor()

c.execute("select distinct(rollcallid) from rollcalls;")
calls = c.fetchall()
calls = [x[0] for x in calls]
calls = [int(x.split(".")[1]) for x in calls]
calls = sorted(list(set(calls)))


pprint(calls)
