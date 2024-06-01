import pandas as pd
import requests
import json
from pprint import pprint

df = pd.read_csv("politifact_claims.csv")

# cos similarity models -
# msmarco-MiniLM-L-6-v3
# msmarco-MiniLM-L-12-v3
# msmarco-distilbert-base-v3
# msmarco-distilbert-base-v4
# msmarco-roberta-base-v3

# dot product models -
# msmarco-distilbert-base-dot-prod-v3
# msmarco-roberta-base-ance-firstp
# msmarco-distilbert-base-tas-b

models = [
    # cos similarity models
    "msmarco-MiniLM-L-6-v3",
    "msmarco-MiniLM-L-12-v3",
    "msmarco-distilbert-base-v3",
    "msmarco-distilbert-base-v4",
    "msmarco-roberta-base-v3",
    # dot product models
    "msmarco-distilbert-base-dot-prod-v3",
    "msmarco-roberta-base-ance-firstp",
    "msmarco-distilbert-base-tas-b",
]

# cos similarity models
# model = models[0]
# model = models[1]
# model = models[2]
# model = models[3]
model = models[4]
# dot product models
# model = models[5]
# model = models[6]
# model = models[7]

for i, claim in enumerate(df["claim_entered"]):
    url = "http://127.0.0.1:8000/api?claim=" + claim + "&model_name=" + model

    bill_titles = []

    response = requests.get(url)

    if response.status_code != 200:
        df.loc[i, model] = str(response.status_code) + "_error"
        continue

    with open("response.json", "w") as file:
        json.dump(response.json(), file)
    with open("response.json", "r") as file:
        data = json.load(file)

    if not data["bills"]:
        df.loc[i, model] = "no_bill_found"
        continue

    for entity in data["bills"]:
        bill_titles.append(entity["bill_title"])

    df.loc[i, model] = str(bill_titles)


df.to_csv("politifact_claims.csv", index=False)
