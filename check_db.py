import sqlite3

conn = sqlite3.connect("data/database/cleaned_campaigns.db")
cursor = conn.cursor()

print("\nTABLES:")
print(cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())

print("\nVIEWS:")
print(cursor.execute("SELECT name FROM sqlite_master WHERE type='view';").fetchall())

conn.close()
