import pandas as pd
from pprint import pprint

df = pd.read_csv("politifact_claims.csv")

models = [
    "msmarco-MiniLM-L-6-v3",
    "msmarco-MiniLM-L-12-v3",
    "msmarco-distilbert-base-v3",
    "msmarco-distilbert-base-v4",
    "msmarco-roberta-base-v3",
    "msmarco-distilbert-base-dot-prod-v3",
    "msmarco-roberta-base-ance-firstp",
    "msmarco-distilbert-base-tas-b",
]

scores = {}
for model in models:
    scores[model] = 0

for model in models:
    cnt = 0
    sum_frac = 0

    for i, bills in enumerate(df["sourced_bills"]):
        if df.loc[i, model] == "no_bill_found":
            continue

        sourced_bills = eval(bills)
        bills_found = eval(df.loc[i, model])
        overlap = len(set(sourced_bills) & set(bills_found))
        sum_frac += overlap / len(sourced_bills)
        cnt += 1

    scores[model] = sum_frac / cnt


pprint(scores)
