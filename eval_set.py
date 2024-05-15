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

models = [
    "msmarco-MiniLM-L-6-v3",
    "msmarco-MiniLM-L-12-v3",
    "msmarco-distilbert-base-v3",
    "msmarco-distilbert-base-v4",
    "msmarco-roberta-base-v3",
]

for model in models:
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


"""
soup = BeautifulSoup(response, "html.parser")
all_titles = soup.find_all("li", class_="results-column-description")
bill_titles = []
for title in all_titles:
    if title.text.split(":")[0] == "Bill Title":
        bill_titles.append(title.text.split(":")[1].strip())
        if bill_titles == []:
            df.loc[i, "bills_found"] = "no_bill_found"
        else:
            df.loc[i, "bills_found"] = str(bill_titles)
"""
