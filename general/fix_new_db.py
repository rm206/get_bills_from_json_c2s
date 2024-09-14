import sqlite3
import pandas as pd
from collections import defaultdict

conn = sqlite3.connect("congress.db")
c = conn.cursor()

c.execute("SELECT rollcallid, memberid, billid from rollcalls")
rollcalls = c.fetchall()

d = defaultdict(list)

for rollcall in rollcalls:
    d[(rollcall[1], rollcall[2])].append(rollcall[0])

for key, val in d.items():
    if len(val) > 1:
        print(key, val)

# for key, val in d.items():
#     if len(val) > 1:
#         temp = [int(v.split("-")[-1]) for v in val]
#         do_not_delete_index = temp.index(max(temp))
#         print(key, val)
#         print(do_not_delete_index)
#         for i, v in enumerate(val):
#             if i != do_not_delete_index:
#                 c.execute(
#                     f"DELETE FROM rollcalls WHERE rollcallid = '{v}' and memberid = '{key[0]}' and billid = '{key[1]}'"
#                 )
#                 conn.commit()
