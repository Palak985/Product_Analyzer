import sqlite3

conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(analysis_history)")
columns = [(row[1], row[2]) for row in cursor.fetchall()]
print("analysis_history columns:")
for col_name, col_type in columns:
    print(f"  {col_name}: {col_type}")
conn.close()
