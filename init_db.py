#!/usr/bin/env python3
"""
Initialize the Flask database with proper schema
Run this before starting the Flask app
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, db
    
    print("Initializing Flask database...")
    
    with app.app_context():
        # Create all tables based on models
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Verify tables were created
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\nCreated tables: {tables}")
        
        if 'analysis_result' in tables:
            columns = [col['name'] for col in inspector.get_columns('analysis_result')]
            print(f"analysis_result columns: {columns}")
            
            # Verify new columns exist
            if 'is_shared' in columns and 'shared_at' in columns:
                print("✓ New peer analyst columns verified!")
            else:
                print("⚠️  Missing columns in analysis_result")
        
        if 'analyst_profile' in tables:
            print("✓ analyst_profile table created!")
        
        print("\n✅ Database initialization complete!")
        print("You can now start the Flask app.")
        
except Exception as e:
    print(f"❌ Error initializing database: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
