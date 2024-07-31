import pandas as pd
import requests
import json
from pprint import pprint

df = pd.read_csv("fsp_kdd.csv")

model = "x"

for i, claim in enumerate(df["claim_entered"]):
    claim = df.loc[i, "claim_entered"]

    url = "http://127.0.0.1:8000/api?claim=" + claim + "&model_name=" + model

    response = requests.get(url)

    if response.status_code != 200:
        df.loc[i, model] = str(response.status_code) + "_error"

    with open("response.json", "w") as file:
        json.dump(response.json(), file)
    with open("response.json", "r") as file:
        data = json.load(file)

    if not data["frame_elements"]:
        df.loc[i, "agent_i"] = str([-1, -1])
        df.loc[i, "issue_i"] = str([-1, -1])
        df.loc[i, "position_i"] = str([-1, -1])
        df.loc[i, "agent_fsp"] = "no_agent"
        df.loc[i, "issue_fsp"] = "no_issue"
        df.loc[i, "position_fsp"] = "no_position"
        continue

    agent_i = [
        data["frame_elements"]["Agent"]["start"],
        data["frame_elements"]["Agent"]["end"],
    ]
    issue_i = [
        data["frame_elements"]["Issue"]["start"],
        data["frame_elements"]["Issue"]["end"],
    ]
    position_i = [
        data["frame_elements"]["Position"]["start"],
        data["frame_elements"]["Position"]["end"],
    ]

    df.loc[i, "agent_i"] = str(agent_i)
    df.loc[i, "issue_i"] = str(issue_i)
    df.loc[i, "position_i"] = str(position_i)

    agent_fsp = claim[agent_i[0] : agent_i[1]] if agent_i[0] != -1 else "no_agent"
    issue_fsp = claim[issue_i[0] : issue_i[1]] if issue_i[0] != -1 else "no_issue"
    position_fsp = (
        claim[position_i[0] : position_i[1]] if position_i[0] != -1 else "no_position"
    )

    df.loc[i, "agent_fsp"] = agent_fsp
    df.loc[i, "issue_fsp"] = issue_fsp
    df.loc[i, "position_fsp"] = position_fsp

    print(f"Agent: {agent_fsp} | Issue: {issue_fsp} | Position: {position_fsp}")

df.to_csv("fsp_kdd.csv", index=False)
