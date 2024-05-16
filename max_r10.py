import pandas as pd
import sqlite3
from pprint import pprint


def query_database(query: str, db: sqlite3.Connection):
    # Query voteview database with given query
    # Input: query (str)
    #        db (sqlite3.Connection)
    # Output: result of query

    cur = db.cursor()
    cur.execute(query)

    return cur.fetchall()


def connect_to_db(db_file: str) -> sqlite3.Connection:
    return sqlite3.connect(db_file)


conn = connect_to_db("congress.db")
df = pd.read_csv("politifact_claims.csv")

all_bills = query_database(
    "SELECT BillCongress, BillType, BillNumber FROM bills;", conn
)
all_bills = [f"{x[0]} {x[1]} {x[2]}" for x in all_bills]

s = 0
cnt = 0

for i, bills in enumerate(df["sourced_bills"]):
    sourced_bills = eval(bills)

    if len(sourced_bills) > 0:
        cnt += 1
        t = 0
        for bill in sourced_bills:
            if bill in all_bills:
                t += 1

        s += t / len(sourced_bills)


print(s / cnt)

conn.close()
