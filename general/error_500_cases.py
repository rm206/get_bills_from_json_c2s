import pandas as pd
import requests
import json

df = pd.read_csv("entered_claims.csv")

i = 0
for i, claim in enumerate(df["claim_entered"]):
    current_content = df["bills_found"][i]

    if current_content == "500_error":
        url = "http://127.0.0.1:8000?claim=" + claim
        # assert (
        #     url
        #     == "http://127.0.0.1:8000?claim=Senator Cryin Chuck Schumer fought hard against the Bad Iran Deal even going at it with President Obama, %26 then Voted against it!"
        # )

        print(url)
        print("~~~")
        print(
            "http://127.0.0.1:8000?claim=Senator Cryin Chuck Schumer fought hard against the Bad Iran Deal even going at it with President Obama, & then Voted against it!"
        )
        url = "http://127.0.0.1:8000?claim=Senator Cryin Chuck Schumer fought hard against the Bad Iran Deal even going at it with President Obama, %26 then Voted against it!"
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
