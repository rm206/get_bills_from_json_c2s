import pandas as pd
import requests
import json

df = pd.read_csv("entered_claims.csv")

skips = []
with open("skip.txt", "r") as file:
    s = file.read()
    skips = s.split()

skips = [int(j) for j in skips]

i = 0
for i, claim in enumerate(df["claim_entered"]):
    if i in skips:
        url = "http://127.0.0.1:8000?claim=" + claim
        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                df.loc[i, "bills_found"] = str(response.status_code) + "_error"
                print(f"[{i+2}] status code error: {response.status_code}")
                continue

            with open("response.json", "w") as file:
                json.dump(response.json(), file)

            with open("response.json", "r") as file:
                data = json.load(file)

            if not data["bills"]:
                df.loc[i, "bills_found"] = "no_bill_found"
                print(f"[{i+2}] no bill found")
                continue

            s = ""
            for j, bill in enumerate(data["bills"]):
                if j == len(data["bills"]) - 1:
                    s += bill["bill_title"]
                else:
                    s += bill["bill_title"] + ", "
            df.loc[i, "bills_found"] = s
            print(f"[{i+2}] done")

        except requests.exceptions.Timeout:
            df.loc[i, "bills_found"] = "Request_timed_out"
            print(f"[{i+2}] timed out")
            with open("skip.txt", "a") as file:
                file.write("\n" + str(i) + "\n")

            break

df.to_csv("entered_claims.csv", index=False)
