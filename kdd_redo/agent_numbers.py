import pandas as pd

df = pd.read_csv("kdd.csv")

right_count = 0
wrong_count = 0
no_agent_count = 0
total_count = 0

for i, agent_found in enumerate(df["agent_found"]):
    id_found = df.loc[i, "id_found"].lower()
    real_id = df.loc[i, "real_id"].lower()

    if id_found == "no_agent_found":
        no_agent_count += 1
    elif id_found == real_id:
        right_count += 1
    else:
        wrong_count += 1

    total_count += 1

print("right percentage (total):", right_count / total_count)
print(
    "right percentage (excluding no_agent_found):",
    right_count / (total_count - no_agent_count),
)
