import sqlite3
from pprint import pprint
from rank_bm25 import BM25Okapi, BM25L, BM25Plus
import pandas as pd

df = pd.read_csv("politifact_claims.csv")


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

corpus = query_database("SELECT BillID, BillDescription FROM bills;", conn)
all_bills_ids = [x[0] for x in corpus]
all_bills = [x[1] for x in corpus]

all_bills = [doc.lower() for doc in all_bills]
tokenized_all_bills = [doc.split(" ") for doc in all_bills]

bm25Okapi = BM25Okapi(tokenized_all_bills)
bm25L = BM25L(tokenized_all_bills)
bm25Plus = BM25Plus(tokenized_all_bills)

variants = ["bm25Okapi", "bm25L", "bm25Plus"]

for variant in variants:
    for i, claim in enumerate(df["claim_entered"]):
        claim = claim.lower()
        tokenized_claim = claim.split(" ")
        if variant == "bm25Okapi":
            top_10 = bm25Okapi.get_top_n(tokenized_claim, all_bills, n=10)
        elif variant == "bm25L":
            top_10 = bm25L.get_top_n(tokenized_claim, all_bills, n=10)
        elif variant == "bm25Plus":
            top_10 = bm25Plus.get_top_n(tokenized_claim, all_bills, n=10)

        top10_bills_ids = [all_bills_ids[all_bills.index(t)] for t in top_10]
        top10_bills_titles = [
            query_database(
                f"SELECT BillCongress, BillType, BillNumber FROM bills WHERE BillID = {bill_id};",
                conn,
            )
            for bill_id in top10_bills_ids
        ]
        top10_bills_titles = [
            f"{x[0][0]} {x[0][1]} {x[0][2]}" for x in top10_bills_titles
        ]

        df.loc[i, variant] = str(top10_bills_titles)

df.to_csv("politifact_claims.csv", index=False)

conn.close()
