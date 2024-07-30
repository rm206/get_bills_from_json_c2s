import pandas as pd
import requests
import json


df = pd.read_csv("kdd.csv")
model = "x"

for i, claim in enumerate(df["claim_entered"]):
    url = "http://127.0.0.1:8000/api?claim=" + claim + "&model_name=" + model

    response = requests.get(url)

    if response.status_code != 200:
        df.loc[i, model] = str(response.status_code) + "_error"
        continue

    with open("response.json", "w") as file:
        json.dump(response.json(), file)
    with open("response.json", "r") as file:
        data = json.load(file)

    if not data["member_id"] or not data["congress_member"]:
        df.loc[i, "agent_found"] = "no_agent_found"
        df.loc[i, "id_found"] = "no_agent_found"
        continue

    df.loc[i, "agent_found"] = str(data["congress_member"])
    df.loc[i, "id_found"] = str(data["member_id"])


df.to_csv("kdd.csv", index=False)
