#!/usr/bin/env python3
# init_db.py
# Initialize PostgreSQL database for Perpetual Ideas Machine

import os
from database import init_db
from dotenv import load_dotenv

load_dotenv()

def main():
    """Initialize the database"""
    print("🗄️  Initializing Perpetual Ideas Machine database...")
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable not set")
        print("   Please set DATABASE_URL in your .env file")
        print("   Example: DATABASE_URL=postgresql://user:password@localhost:5432/pim_db")
        return 1
    
    try:
        init_db()
        print("✅ Database initialized successfully!")
        return 0
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize database: {e}")
        return 1

if __name__ == '__main__':
    exit(main())

