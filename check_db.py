import sqlite3
import os

# Check both databases
for db in ['app.db', 'instance/app.db']:
    if os.path.exists(db):
        print(f"\n{db}:")
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"  Tables: {tables}")
        
        if 'analysis_result' in tables:
            cursor.execute("PRAGMA table_info(analysis_result)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"  Columns in analysis_result: {columns}")
        conn.close()
