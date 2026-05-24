import sqlite3

conn = sqlite3.connect("data/database/cleaned_campaigns.db")

with open("sql/schema.sql", "r", encoding="utf-8") as f:
    schema = f.read()

conn.executescript(schema)

conn.commit()

print("Schema executed successfully")

conn.close()
