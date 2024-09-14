import sqlite3

conn = sqlite3.connect("congress.db")
curr = conn.cursor()

# fix the interchanged column name
curr.execute("ALTER TABLE bills RENAME COLUMN BillDescription TO TempColumn;")
curr.execute("ALTER TABLE bills RENAME COLUMN BillSummary TO BillDescription;")
curr.execute("ALTER TABLE bills RENAME COLUMN TempColumn TO BillSummary;")

# populate billdescription with billsummary where billdescription is missing now
curr.execute(
    "UPDATE Bills SET BillDescription = BillSummary WHERE BillDescription IS NULL OR BillDescription = '';"
)

# delete bill with id 124200 as it has all cols null
curr.execute("DELETE FROM Bills WHERE BillID = 124200;")

curr.commit()
