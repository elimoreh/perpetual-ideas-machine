#!/usr/bin/env python3
"""
Quick setup checker for Perpetual Ideas Machine
Tells you what's missing and how to fix it
"""

import os
import sys
from pathlib import Path

def check_setup():
    """Check what's needed to run the app"""
    print("🔍 Checking Perpetual Ideas Machine setup...\n")
    
    issues = []
    warnings = []
    
    # Check 1: Virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
    else:
        issues.append("Virtual environment not activated")
        print("❌ Virtual environment not activated")
        print("   Fix: source venv/bin/activate\n")
    
    # Check 2: .env file exists
    env_path = Path('.env')
    if env_path.exists():
        print("✅ .env file exists")
    else:
        issues.append(".env file missing")
        print("❌ .env file missing")
        print("   Fix: cp env.example .env\n")
        return  # Can't check further without .env
    
    # Check 3: Load .env
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check 4: API Key
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if openai_key and openai_key != 'sk-your-openai-api-key-here':
        print("✅ OpenAI API key is set")
    elif anthropic_key and anthropic_key != 'sk-ant-your-anthropic-api-key-here':
        print("✅ Anthropic API key is set")
    else:
        issues.append("No valid API key")
        print("❌ No valid API key found")
        print("   Fix: Edit .env and add your OPENAI_API_KEY or ANTHROPIC_API_KEY\n")
    
    # Check 5: DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print(f"✅ DATABASE_URL is set")
        
        # Try to connect
        try:
            import psycopg2
            from urllib.parse import urlparse
            
            # Parse URL
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            
            # Try connection
            conn = psycopg2.connect(database_url)
            conn.close()
            print("✅ Database connection successful")
        except ImportError:
            issues.append("psycopg2 not installed")
            print("❌ psycopg2 not installed")
            print("   Fix: pip install psycopg2-binary\n")
        except Exception as e:
            issues.append("Cannot connect to database")
            print(f"❌ Cannot connect to database: {e}")
            print("   Fix: Make sure PostgreSQL is running")
            print("   Local: brew services start postgresql@15")
            print("   Or use a cloud database (see README_NOW.md)\n")
    else:
        issues.append("DATABASE_URL not set")
        print("❌ DATABASE_URL not set")
        print("\n   You have 3 options:")
        print("\n   Option 1 - Free Cloud Database (EASIEST):")
        print("   1. Go to https://neon.tech or https://elephantsql.com")
        print("   2. Sign up (free)")
        print("   3. Create a database")
        print("   4. Copy connection string")
        print("   5. Add to .env: DATABASE_URL=postgresql://...")
        print("\n   Option 2 - Local PostgreSQL:")
        print("   1. brew install postgresql@15")
        print("   2. brew services start postgresql@15")
        print("   3. createdb pim_db")
        print("   4. Add to .env: DATABASE_URL=postgresql://localhost:5432/pim_db")
        print("\n   Option 3 - Deploy to Heroku only:")
        print("   See DEPLOYMENT.md\n")
    
    # Check 6: Dependencies
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        issues.append("Flask not installed")
        print("❌ Flask not installed")
        print("   Fix: pip install -r requirements.txt\n")
    
    # Summary
    print("\n" + "="*60)
    if not issues:
        print("✅ ALL CHECKS PASSED! You're ready to run:")
        print("\n   python app.py")
        print("\n   Then visit: http://localhost:5000")
    else:
        print(f"❌ Found {len(issues)} issue(s) to fix:\n")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print("\n📖 For detailed help, see: README_NOW.md")
        print("📖 For database setup: DATABASE_SETUP.md")
    print("="*60)

if __name__ == '__main__':
    try:
        check_setup()
    except Exception as e:
        print(f"\n❌ Error during setup check: {e}")
        print("\nPlease check that you're in the PIM directory and have run:")
        print("  source venv/bin/activate")

