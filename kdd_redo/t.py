import pandas as pd

df = pd.read_csv("fsp_kdd.csv")

for i, agent_fsp in enumerate(df["agent_fsp"]):
    issue_fsp = df.loc[i, "issue_fsp"]
    position_fsp = df.loc[i, "position_fsp"]

    if agent_fsp == "no_agent":
        df.loc[i, "agent_correct"] = -1
    if issue_fsp == "no_issue":
        df.loc[i, "issue_correct"] = -1
    if position_fsp == "no_position":
        df.loc[i, "position_correct"] = -1

df.to_csv("fsp_kdd.csv", index=False)
