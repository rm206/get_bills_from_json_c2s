import pandas as pd

df = pd.read_csv("entered_claims.csv")

i = 0
for i, claim in enumerate(df["claim_entered"]):
    if df["bills_found"][i] == "no_bill_found":
        print(claim)
        print()
