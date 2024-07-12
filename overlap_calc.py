import pandas as pd
from pprint import pprint

df = pd.read_csv("politifact_claims.csv")

models = [
    "msmarco-MiniLM-L-6-v3",
    "msmarco-MiniLM-L-12-v3",
    "msmarco-distilbert-base-v3",
    "msmarco-distilbert-base-v4",
    "msmarco-roberta-base-v3",
    "msmarco-distilbert-base-dot-prod-v3",
    "msmarco-roberta-base-ance-firstp",
    "msmarco-distilbert-base-tas-b",
    "bm25Okapi",
    "bm25L",
    "bm25Plus",
    "mixedbread-ai/mxbai-embed-large-v1_cossim",
    "WhereIsAI/UAE-Large-V1_cossim",
    "Snowflake/snowflake-arctic-embed-l_cossim",
    "mixedbread-ai/mxbai-embed-large-v1_dotprod",
    "WhereIsAI/UAE-Large-V1_dotprod",
    "Snowflake/snowflake-arctic-embed-l_dotprod",
]

# model_dict = {
#     "msmarco-MiniLM-L-6-v3": 1,
#     "msmarco-MiniLM-L-12-v3": 1,
#     "msmarco-distilbert-base-v3": 1,
#     "msmarco-distilbert-base-v4": 1,
#     "msmarco-roberta-base-v3": 1,
#     "msmarco-distilbert-base-dot-prod-v3": 2,
#     "msmarco-roberta-base-ance-firstp": 2,
#     "msmarco-distilbert-base-tas-b": 2,
#     "bm25Okapi": 0,
#     "bm25L": 0,
#     "bm25Plus": 0,
#     "mixedbread-ai/mxbai-embed-large-v1": 3,
# }

scores = {}
for model in models:
    scores[model] = 0

for model in models:
    cnt = 0
    sum_frac = 0

    for i, bills in enumerate(df["sourced_bills"]):
        if (
            df.loc[i, model] == "no_bill_found"
            or df.loc[i, model] == "no_bills"
            or df.loc[i, model] == "no_agent"
            or df.loc[i, model] == "no_issue"
        ):
            continue

        sourced_bills = eval(bills)
        bills_found = eval(df.loc[i, model])
        overlap = len(set(sourced_bills) & set(bills_found))
        sum_frac += overlap / len(sourced_bills)
        cnt += 1

    scores[model] = sum_frac / cnt


scores_list = [[k, v] for k, v in scores.items()]
scores_list.sort(key=lambda x: x[1], reverse=True)
scores_list = [[k, round(v, 4)] for k, v in scores.items()]
scores_list.sort(key=lambda x: x[1], reverse=True)
pprint(scores_list)


# sum_1s = 0
# sum_2s = 0
# sum_3s = 0
# for model, score in scores_list:
#     if model_dict[model] == 1:
#         sum_1s += score
#     elif model_dict[model] == 2:
#         sum_2s += score
#     elif model_dict[model] == 3:
#         sum_3s += score

# print("cos sim", sum_1s / 5)
# print("dot prod", sum_2s / 3)
# print("new models", sum_3s / 1)


# overlaps = {}
# for model in models:
#     overlaps[model] = []

# for model in models:
#     for i, bills in enumerate(df["sourced_bills"]):
#         if (
#             df.loc[i, model] == "no_bill_found"
#             or df.loc[i, model] == "no_bills"
#             or df.loc[i, model] == "no_agent"
#             or df.loc[i, model] == "no_issue"
#         ):
#             continue

#         sourced_bills = eval(bills)
#         bills_found = eval(df.loc[i, model])
#         overlap = len(set(sourced_bills) & set(bills_found))
#         overlaps[model].append(overlap)

# overlaps_list = [[k, v] for k, v in overlaps.items()]
# overlaps_list.sort(key=lambda x: sum(x[1]), reverse=True)
# for model, overlap in overlaps_list:
#     print(model, overlap)
