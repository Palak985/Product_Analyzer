#!/usr/bin/env python3
"""
Database migration script to add missing columns and tables
"""
import sqlite3
import os

def migrate_database():
    """Migrate database to add missing columns"""
    
    # Find the database file
    db_paths = ['instance/app.db', 'app.db', 'instance/reviews.db']
    db_path = None
    
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("ERROR: Database file not found!")
        print(f"Searched for: {db_paths}")
        return False
    
    print(f"Connecting to database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # First, check what tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Existing tables: {tables}\n")
        
        # Check if analysis_result table exists
        if 'analysis_result' in tables:
            print("Found 'analysis_result' table")
            cursor.execute("PRAGMA table_info(analysis_result)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"Current columns: {columns}")
            
            # Add is_shared column if missing
            if 'is_shared' not in columns:
                print("  → Adding 'is_shared' column...")
                cursor.execute("ALTER TABLE analysis_result ADD COLUMN is_shared BOOLEAN DEFAULT 1")
                print("  ✓ Added 'is_shared'")
            
            # Add shared_at column if missing
            if 'shared_at' not in columns:
                print("  → Adding 'shared_at' column...")
                cursor.execute("ALTER TABLE analysis_result ADD COLUMN shared_at DATETIME DEFAULT NULL")
                print("  ✓ Added 'shared_at'")
        else:
            print("⚠️  'analysis_result' table NOT found in database")
            print("   The table will be created automatically by Flask when app starts")
        
        # Check if analyst_profile table exists
        if 'analyst_profile' not in tables:
            print("\nCreating 'analyst_profile' table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analyst_profile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    specialty VARCHAR(200) DEFAULT 'General Analysis',
                    bio TEXT DEFAULT '',
                    total_analyses INTEGER DEFAULT 0,
                    avg_sentiment_score FLOAT DEFAULT 0.0,
                    FOREIGN KEY(user_id) REFERENCES user(id)
                )
            """)
            print("✓ Created 'analyst_profile' table")
        else:
            print("\n✓ 'analyst_profile' table already exists")
        
        conn.commit()
        
        # Verify final state
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"\nFinal tables: {tables}")
        
        if 'analysis_result' in tables:
            cursor.execute("PRAGMA table_info(analysis_result)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"Final analysis_result columns: {columns}")
        
        conn.close()
        print("\n✅ Database migration completed!")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    migrate_database()
