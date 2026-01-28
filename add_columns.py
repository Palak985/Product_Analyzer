#!/usr/bin/env python3
"""
Directly add missing columns to the existing database
"""
import sqlite3
import os

db_path = 'instance/reviews.db'

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

print(f"Connecting to {db_path}...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check current columns
cursor.execute("PRAGMA table_info(analysis_result)")
columns = {row[1]: row[2] for row in cursor.fetchall()}
print(f"Current columns: {list(columns.keys())}")

# Add missing columns
if 'is_shared' not in columns:
    print("Adding is_shared column...")
    cursor.execute("ALTER TABLE analysis_result ADD COLUMN is_shared BOOLEAN DEFAULT 1 NOT NULL")
    print("✓ Added is_shared")

if 'shared_at' not in columns:
    print("Adding shared_at column...")
    cursor.execute("ALTER TABLE analysis_result ADD COLUMN shared_at DATETIME DEFAULT NULL")
    print("✓ Added shared_at")

conn.commit()

# Verify
cursor.execute("PRAGMA table_info(analysis_result)")
columns = [row[1] for row in cursor.fetchall()]
print(f"\nFinal columns: {columns}")

if 'is_shared' in columns and 'shared_at' in columns:
    print("\n✅ All columns added successfully!")
else:
    print("\n❌ Failed to add columns")

conn.close()
