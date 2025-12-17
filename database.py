# database.py
# PostgreSQL database management for Perpetual Ideas Machine

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Get PostgreSQL database connection"""
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        raise ValueError(
            "DATABASE_URL not set in environment.\n"
            "For local development, you need PostgreSQL installed.\n"
            "See DATABASE_SETUP.md for setup instructions.\n\n"
            "Quick setup:\n"
            "  brew install postgresql@15\n"
            "  brew services start postgresql@15\n"
            "  createdb pim_db\n"
            "  echo 'DATABASE_URL=postgresql://localhost:5432/pim_db' >> .env"
        )
    
    # Heroku uses postgres://, but psycopg2 requires postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
    return conn


def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create inventions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventions (
            id SERIAL PRIMARY KEY,
            invention_id VARCHAR(255) UNIQUE NOT NULL,
            domain_key VARCHAR(255) NOT NULL,
            domain_name VARCHAR(255) NOT NULL,
            title TEXT,
            content TEXT NOT NULL,
            hash VARCHAR(64) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_domain_key ON inventions(domain_key)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_created_at ON inventions(created_at)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_invention_id ON inventions(invention_id)
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database initialized")


def save_invention(invention_id, domain_key, domain_name, title, content, hash_value):
    """Save invention to database"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO inventions (invention_id, domain_key, domain_name, title, content, hash)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (invention_id) DO UPDATE
            SET content = EXCLUDED.content,
                title = EXCLUDED.title,
                hash = EXCLUDED.hash
        """, (invention_id, domain_key, domain_name, title, content, hash_value))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def get_invention(domain_key, invention_id):
    """Get a specific invention"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT * FROM inventions
        WHERE domain_key = %s AND invention_id = %s
    """, (domain_key, invention_id))
    
    result = cur.fetchone()
    cur.close()
    conn.close()
    
    return dict(result) if result else None


def get_inventions_by_domain(domain_key, limit=None):
    """Get all inventions for a domain"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = """
        SELECT invention_id as id, invention_id, domain_key, domain_name, title, 
               LEFT(content, 300) as preview, created_at,
               DATE(created_at) as date
        FROM inventions
        WHERE domain_key = %s
        ORDER BY created_at DESC
    """
    
    if limit:
        query += f" LIMIT {limit}"
    
    cur.execute(query, (domain_key,))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return [dict(row) for row in results]


def get_all_inventions(limit=100):
    """Get all inventions across all domains"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT invention_id as id, invention_id, domain_key, domain_name, title,
               LEFT(content, 200) as preview, created_at,
               DATE(created_at) as date
        FROM inventions
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return [dict(row) for row in results]


def search_inventions(query):
    """Search inventions by content"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    search_term = f"%{query}%"
    
    cur.execute("""
        SELECT invention_id as id, invention_id, domain_key, domain_name, title, content, created_at,
               DATE(created_at) as date
        FROM inventions
        WHERE LOWER(content) LIKE LOWER(%s) OR LOWER(title) LIKE LOWER(%s)
        ORDER BY created_at DESC
        LIMIT 50
    """, (search_term, search_term))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return [dict(row) for row in results]


def count_inventions_by_domain(domain_key):
    """Count inventions in a domain"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT COUNT(*) as count
        FROM inventions
        WHERE domain_key = %s
    """, (domain_key,))
    
    result = cur.fetchone()
    cur.close()
    conn.close()
    
    return result['count'] if result else 0


def get_stats():
    """Get overall statistics"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Total inventions
    cur.execute("SELECT COUNT(*) as total FROM inventions")
    total = cur.fetchone()['total']
    
    # Count by domain
    cur.execute("""
        SELECT domain_key, COUNT(*) as count
        FROM inventions
        GROUP BY domain_key
    """)
    by_domain = {row['domain_key']: row['count'] for row in cur.fetchall()}
    
    # Active domains
    domains_active = len(by_domain)
    
    cur.close()
    conn.close()
    
    return {
        'total_inventions': total,
        'domains_active': domains_active,
        'by_domain': by_domain
    }

