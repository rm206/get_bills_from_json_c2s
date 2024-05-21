import pandas as pd
import sqlite3
from pprint import pprint
import requests
import json


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

s = 0
cnt = 0

for i, bills in enumerate(df["sourced_bills"]):
    sourced_bills = eval(bills)

    url = (
        "http://127.0.0.1:8000/api?claim="
        + df.loc[i, "claim_entered"]
        + "&model_name="
        + "model"
    )

    response = requests.get(url)

    if response.status_code != 200:
        continue

    with open("response.json", "w") as file:
        json.dump(response.json(), file)
    with open("response.json", "r") as file:
        data = json.load(file)

    if not data["member_id"] or not data["congress_member"]:
        continue

    member_id = data["member_id"]

    all_bills = query_database(
        f"SELECT bills.BillCongress, bills.BillType, bills.BillNumber FROM bills WHERE bills.BillID in (SELECT DISTINCT(BillID) FROM Rollcalls WHERE MemberID = '{member_id}');",
        conn,
    )
    all_bills = [f"{x[0]} {x[1]} {x[2]}" for x in all_bills]

    if len(sourced_bills) > 0:
        cnt += 1
        t = 0
        for bill in sourced_bills:
            if bill in all_bills:
                t += 1

    s += t / len(sourced_bills)

print(s / cnt)

"""
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
"""
