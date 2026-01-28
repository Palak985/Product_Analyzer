#!/usr/bin/env python3
"""
Debug script to check what SQLAlchemy sees in the model
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Clear any cached modules
if 'app' in sys.modules:
    del sys.modules['app']

from app import AnalysisResult, db

print("Checking AnalysisResult model attributes:")
print(f"Table name: {AnalysisResult.__tablename__}")
print("\nColumns defined in model:")
for column in AnalysisResult.__table__.columns:
    print(f"  - {column.name}: {column.type}")

print("\nChecking if is_shared is in model:")
print(f"  hasattr(AnalysisResult, 'is_shared'): {hasattr(AnalysisResult, 'is_shared')}")
print(f"  'is_shared' in [c.name for c in AnalysisResult.__table__.columns]: {'is_shared' in [c.name for c in AnalysisResult.__table__.columns]}")
