import sqlite3
from collections import defaultdict

conn = sqlite3.connect("congress.db")
c = conn.cursor()


"""
c.execute("SELECT rollcallid, memberid, billid from rollcalls")

rollcalls = c.fetchall()

d = defaultdict(list)

for rollcall in rollcalls:
    d[(rollcall[1], rollcall[2])].append(rollcall[0])

for key, value in d.items():
    if len(value) > 1:
        print(key, value)
"""

"""
c.execute("SELECT name from members")
members = c.fetchall()

d = {}
for member in members:
    d[member[0]] = d.get(member[0], 0) + 1

for key, value in d.items():
    if value > 1:
        print(key, value)
"""

c.execute("select billid, billsummary from bills limit 1000")
bills = c.fetchall()

d = defaultdict(list)
for bill in bills:
    d[bill[1]].append(bill[0])

for key, value in d.items():
    if len(value) > 1:
        print(key)
        print(value)
        print()
