import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint

df = pd.read_csv("politifact_claims.csv")


for i, claim in enumerate(df["claim_entered"]):
    url = "https://idir.uta.edu/claimlens/submit?query=" + claim

    response = requests.get(url, timeout=20).text
    soup = BeautifulSoup(response, "html.parser")
    all_titles = soup.find_all("li", class_="results-column-description")
    bill_titles = []
    for title in all_titles:
        if title.text.split(":")[0] == "Bill Title":
            bill_titles.append(title.text.split(":")[1].strip())

    if bill_titles == []:
        df.loc[i, "bills_found"] = "no_bill_found"
    else:
        df.loc[i, "bills_found"] = str(bill_titles)

df.to_csv("politifact_claims.csv", index=False)

# from bs4 import BeautifulSoup
# from pprint import pprint

# with open("response.html", "r") as file:
#     data = file.read()

# soup = BeautifulSoup(data, "html.parser")
# all_titles = soup.find_all("li", class_="results-column-description")
# bill_titles = []
# for title in all_titles:
#     if title.text.split(":")[0] == "Bill Title":
#         bill_titles.append(title.text.split(":")[1].strip())

# pprint(bill_titles)
