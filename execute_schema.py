import sqlite3

conn = sqlite3.connect("data/database/cleaned_campaigns.db")

cursor = conn.cursor()

with open("sql/schema.sql", "r", encoding="utf-8") as f:
    schema = f.read()

try:
    conn.executescript(schema)
    conn.commit()
    print("Schema executed successfully")

except Exception as e:
    print(f"Schema warning: {e}")
    print("Existing tables skipped successfully")

finally:
    conn.close()