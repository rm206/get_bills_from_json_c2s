import sqlite3
from pprint import pprint

conn = sqlite3.connect("congress.db")
c = conn.cursor()

c.execute("select BillSummary from bills;")
rows = c.fetchall()

bills = [row[0] for row in rows]
bills = [len(bill.split()) for bill in bills]

# print(sum(bills) / len(bills))

import pandas as pd

df = pd.read_csv("politifact_claims.csv")

queries = list(df["claim_entered"])
queries = [len(query.split()) for query in queries]

# print(sum(queries) / len(queries))

import matplotlib.pyplot as plt
import seaborn as sns

# create a histogram of numbers of words in bills and queries with seaborn and make it a curve
sns.histplot(bills, kde=True)
sns.histplot(queries, kde=True)
plt.show()
