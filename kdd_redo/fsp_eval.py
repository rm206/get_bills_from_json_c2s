import pandas as pd

df = pd.read_csv("fsp_kdd_eval.csv")

position_total, agent_total, issue_total, total = 0, 0, 0, 0

for i, claim in enumerate(df["claim_entered"]):
    position_correct = df.loc[i, "position_correct"]
    agent_correct = df.loc[i, "agent_correct"]
    issue_correct = df.loc[i, "issue_correct"]

    position_total += position_correct
    agent_total += agent_correct
    issue_total += issue_correct

    total += 1

position_accuracy = position_total / total
agent_accuracy = agent_total / total
issue_accuracy = issue_total / total

print("Position accuracy:", position_accuracy)
print("Agent accuracy:", agent_accuracy)
print("Issue accuracy:", issue_accuracy)
