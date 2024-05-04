import pandas as pd

df = pd.read_csv("politifact_claims.csv")

for i, bills in enumerate(df["sourced_bills"]):
    if df.loc[i, "bills_found"] == "no_bill_found":
        df.loc[i, "overlap"] = "no_bill_found"
        continue

    sourced_bills = eval(bills)
    bills_found = eval(df.loc[i, "bills_found"])

    overlap = len(set(sourced_bills) & set(bills_found))
    df.loc[i, "overlap"] = f"{overlap} of {len(sourced_bills)}"

df.to_csv("politifact_claims.csv", index=False)
