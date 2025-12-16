# database_sqlite.py
# SQLite fallback for local development (does NOT work on Heroku)

import sqlite3
import os
from datetime import datetime

DB_PATH = 'local_inventions.db'

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invention_id TEXT UNIQUE NOT NULL,
            domain_key TEXT NOT NULL,
            domain_name TEXT NOT NULL,
            title TEXT,
            content TEXT NOT NULL,
            hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cur.execute("CREATE INDEX IF NOT EXISTS idx_domain_key ON inventions(domain_key)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON inventions(created_at)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_invention_id ON inventions(invention_id)")
    
    conn.commit()
    conn.close()
    print("✅ SQLite database initialized (local development only)")

def save_invention(invention_id, domain_key, domain_name, title, content, hash_value):
    """Save invention to SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT OR REPLACE INTO inventions 
            (invention_id, domain_key, domain_name, title, content, hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (invention_id, domain_key, domain_name, title, content, hash_value))
        
        conn.commit()
    finally:
        conn.close()

def get_invention(domain_key, invention_id):
    """Get a specific invention"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("""
        SELECT * FROM inventions
        WHERE domain_key = ? AND invention_id = ?
    """, (domain_key, invention_id))
    
    result = cur.fetchone()
    conn.close()
    
    return dict(result) if result else None

def get_inventions_by_domain(domain_key, limit=None):
    """Get all inventions for a domain"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    query = """
        SELECT invention_id as id, invention_id, domain_key, domain_name, title, 
               substr(content, 1, 300) as preview, created_at,
               DATE(created_at) as date
        FROM inventions
        WHERE domain_key = ?
        ORDER BY created_at DESC
    """
    
    if limit:
        query += f" LIMIT {limit}"
    
    cur.execute(query, (domain_key,))
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    
    return results

def get_all_inventions(limit=100):
    """Get all inventions across all domains"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("""
        SELECT invention_id as id, invention_id, domain_key, domain_name, title,
               substr(content, 1, 200) as preview, created_at,
               DATE(created_at) as date
        FROM inventions
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    
    return results

def search_inventions(query):
    """Search inventions by content"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    search_term = f"%{query}%"
    
    cur.execute("""
        SELECT invention_id as id, invention_id, domain_key, domain_name, title, content, created_at,
               DATE(created_at) as date
        FROM inventions
        WHERE LOWER(content) LIKE LOWER(?) OR LOWER(title) LIKE LOWER(?)
        ORDER BY created_at DESC
        LIMIT 50
    """, (search_term, search_term))
    
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    
    return results

def count_inventions_by_domain(domain_key):
    """Count inventions in a domain"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT COUNT(*) as count
        FROM inventions
        WHERE domain_key = ?
    """, (domain_key,))
    
    result = cur.fetchone()
    conn.close()
    
    return result[0] if result else 0

def get_stats():
    """Get overall statistics"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
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
    
    conn.close()
    
    return {
        'total_inventions': total,
        'domains_active': domains_active,
        'by_domain': by_domain
    }

