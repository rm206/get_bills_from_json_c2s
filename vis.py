import pandas as pd
import matplotlib.pyplot as plt

# Sample DataFrame creation
# Replace this with your actual DataFrame loading or creation code
df = pd.read_csv("entered_claims.csv")

# Count the occurrences of each unique value in the column
value_counts = df["bills_found"].value_counts()

# Identify 'found' as any value not explicitly listed
explicit_values = ["no_bill_found", "no_member_id"]
found_count = value_counts[~value_counts.index.isin(explicit_values)].sum()

# Remove these 'found' values from the series and add a new 'found' entry
value_counts = value_counts[explicit_values]
if found_count > 0:
    value_counts["found"] = found_count

# Plotting
plt.figure(figsize=(10, 7))
plt.pie(value_counts, labels=value_counts.index, autopct="%1.1f%%", startangle=140)
plt.title("Distribution of proj pipeline")
plt.show()
