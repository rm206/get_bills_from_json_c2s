import pandas as pd
import requests
import json

df = pd.read_csv("politifact_claims.csv")

models = [
    "mixedbread-ai/mxbai-embed-large-v1_cossim",
    "WhereIsAI/UAE-Large-V1_cossim",
    "Snowflake/snowflake-arctic-embed-l_cossim",
]

model = models[2]

for i, claim in enumerate(df["claim_entered"]):
    url1 = "http://127.0.0.1:8000/api?claim=" + claim + "&model_name=" + model
    url2 = "http://127.0.0.1:8001/api?claim=" + claim

    bill_titles = []

    response1 = requests.get(url1)

    if response1.status_code != 200:
        df.loc[i, model] = str(response1.status_code) + "_error_req1"
        continue

    with open("response1.json", "w") as file:
        json.dump(response1.json(), file)
    with open("response1.json", "r") as file:
        data1 = json.load(file)

    if not data1["member_id"]:
        df.loc[i, model] = "no_agent"
        continue
    if data1["frame_elements"]["Issue"]["start"] == -1:
        df.loc[i, model] = "no_issue"
        continue

    issue_start, issue_end = (
        data1["frame_elements"]["Issue"]["start"],
        data1["frame_elements"]["Issue"]["end"],
    )
    agent_retrieved = data1["member_id"]

    url2 = (
        url2
        + "&issue_fe="
        + (str(issue_start) + "@" + str(issue_end))
        + "&agent_retrieved="
        + agent_retrieved
    )

    response2 = requests.get(url2)

    if response2.status_code != 200:
        df.loc[i, model] = str(response2.status_code) + "_error_req2"
        continue

    with open("response2.json", "w") as file:
        json.dump(response2.json(), file)
    with open("response2.json", "r") as file:
        data2 = json.load(file)

    if not data2["bills"]:
        df.loc[i, model] = "no_bills"
        continue

    bill_titles = [bill["bill_title"] for bill in data2["bills"]]

    df.loc[i, model] = str(bill_titles)

df.to_csv("politifact_claims.csv", index=False)
