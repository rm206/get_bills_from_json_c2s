import pandas as pd
import requests
import json

df = pd.read_csv("colab_stuff.csv")

# models = [
#     "mixedbread-ai/mxbai-embed-large-v1_cossim",
#     "WhereIsAI/UAE-Large-V1_cossim",
#     "Snowflake/snowflake-arctic-embed-l_cossim",
#     "mixedbread-ai/mxbai-embed-large-v1_dotprod",
#     "WhereIsAI/UAE-Large-V1_dotprod",
#     "Snowflake/snowflake-arctic-embed-l_dotprod",
#     "Alibaba-NLP/gte-base-en-v1.5_dotprod",
#     "Alibaba-NLP/gte-base-en-v1.5_cossim",
# ]

models = [
    "stella_en_1.5B_v5_cossim",  # 0
    "stella_en_400M_v5_cossim",  # 1
    "gte-Qwen2-1.5B-instruct_cossim",  # 2
    "gte-large-en-v1.5_cossim",  # 3
    "stella_en_1.5B_v5_dotscore",  # 4
    "stella_en_400M_v5_dotscore",  # 5
    "gte-Qwen2-1.5B-instruct_dotscore",  # 6
    "gte-large-en-v1.5_dotscore",  # 7
]

model = models[0]

for i, claim in enumerate(df["claim_entered"]):
    url1 = "http://127.0.0.1:8000/api?claim=" + claim + "&model_name=" + model
    url2 = "http://127.0.0.1:8001/api?claim=" + claim

    df.loc[i, "part1_claim"] = claim

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
        df.loc[i, "part1_agent"] = "no_agent"
        continue
    if data1["frame_elements"]["Issue"]["start"] == -1:
        df.loc[i, "part1_issue"] = "no_issue"
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

    df.loc[i, "part1_claim"] = claim
    df.loc[i, "part1_agent"] = agent_retrieved
    df.loc[i, "part1_issue"] = str(issue_start) + "@" + str(issue_end)

    """
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

"""
df.to_csv("colab_stuff.csv", index=False)
