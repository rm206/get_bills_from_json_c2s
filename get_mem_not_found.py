import requests
import pandas as pd
import urllib
import json

df = pd.read_csv("entered_claims.csv")

i = 0
for i, claim in enumerate(df["claim_entered"]):
    if df["bills_found"][i] == "no_member_id":

        # claim = urllib.parse.quote_plus(claim)
        print(claim)
        url = "http://127.0.0.1:8000?claim=" + claim

        response = requests.get(url, timeout=10)

        with open("response.json", "w") as file:
            json.dump(response.json(), file)

        with open("response.json", "r") as file:
            data = json.load(file)

        if data["frame_elements"]:
            print(data["frame_elements"]["Agent"])
            start, end = (
                data["frame_elements"]["Agent"]["start"],
                data["frame_elements"]["Agent"]["end"],
            )
            print(claim[start:end])
        else:
            print(data)
        print()
        print()
