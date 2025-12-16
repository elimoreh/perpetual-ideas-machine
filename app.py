# app.py
# Main Flask application for Perpetual Ideas Machine

from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
import json
import random
from generate import generate_invention
from domains import DOMAINS, get_domain_info, get_all_domains
import markdown2
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

load_dotenv()

# Check if DATABASE_URL is set (for PostgreSQL)
database_url = os.getenv('DATABASE_URL')

if database_url:
    # Use PostgreSQL (production/Heroku)
    print("📊 Using PostgreSQL database")
    from database import (
        get_invention, get_inventions_by_domain, get_all_inventions,
        search_inventions as db_search_inventions, count_inventions_by_domain,
        get_stats, init_db
    )
else:
    # Use SQLite (local development fallback)
    print("📊 Using SQLite database (local development only)")
    print("⚠️  Warning: SQLite will NOT work on Heroku!")
    print("   For Heroku deployment, you must set DATABASE_URL")
    print("   See DATABASE_SETUP.md for instructions\n")
    from database_sqlite import (
        get_invention, get_inventions_by_domain, get_all_inventions,
        search_inventions as db_search_inventions, count_inventions_by_domain,
        get_stats, init_db
    )

# Initialize database on startup
try:
    init_db()
except Exception as e:
    print(f"⚠️  Database initialization error: {e}")
    import sys
    sys.exit(1)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Auto-generation configuration
AUTO_GENERATE_ENABLED = os.getenv('AUTO_GENERATE', 'true').lower() == 'true'
AUTO_GENERATE_INTERVAL = int(os.getenv('AUTO_GENERATE_INTERVAL', '3600'))  # 1 hour default

# Initialize scheduler
scheduler = BackgroundScheduler()


def auto_generate_invention():
    """Automatically generate an invention in a random domain"""
    try:
        # Check if we're past February 1, 2026
        cutoff_date = datetime(2026, 2, 1)
        if datetime.utcnow() >= cutoff_date:
            print(f"⏹️  Auto-generation stopped: Reached cutoff date (Feb 1, 2026)")
            scheduler.shutdown()
            return
        
        # Select random domain
        domain_keys = list(DOMAINS.keys())
        domain_key = random.choice(domain_keys)
        domain_info = get_domain_info(domain_key)
        
        # Generate invention
        inv_id = generate_invention(domain_key, domain_info['name'])
        print(f"✅ Auto-generated invention {inv_id} in {domain_info['name']}")
    except Exception as e:
        print(f"❌ Auto-generation error: {str(e)}")


# Start the scheduler
if AUTO_GENERATE_ENABLED:
    # Check if we're already past the cutoff date
    cutoff_date = datetime(2026, 2, 1)
    if datetime.utcnow() >= cutoff_date:
        print(f"⏹️  Auto-generation disabled: Past cutoff date (Feb 1, 2026)")
    else:
        scheduler.add_job(
            func=auto_generate_invention,
            trigger="interval",
            seconds=AUTO_GENERATE_INTERVAL,
            id='auto_generate_job',
            name='Auto-generate inventions',
            replace_existing=True
        )
        scheduler.start()
        days_remaining = (cutoff_date - datetime.utcnow()).days
        print(f"🤖 Auto-generation enabled: every {AUTO_GENERATE_INTERVAL} seconds ({AUTO_GENERATE_INTERVAL/60} minutes)")
        print(f"📅 Will run until February 1, 2026 ({days_remaining} days remaining)")
        
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())


@app.route('/')
def index():
    """Main landing page with domain grid and statistics"""
    try:
        stats = get_stats()
    except Exception as e:
        print(f"Error getting stats: {e}")
        stats = {'total_inventions': 0, 'domains_active': 0, 'by_domain': {}}
    
    return render_template('index.html', 
                         domains=DOMAINS,
                         stats=stats)


@app.route('/domain/<domain_key>')
def view_domain(domain_key):
    """List all inventions for a specific domain"""
    domain_info = get_domain_info(domain_key)
    if not domain_info:
        flash('Domain not found', 'error')
        return redirect(url_for('index'))
    
    try:
        inventions = get_inventions_by_domain(domain_key)
    except Exception as e:
        flash(f'Error loading inventions: {str(e)}', 'error')
        inventions = []
    
    return render_template('domain.html',
                         domain_key=domain_key,
                         domain_info=domain_info,
                         inventions=inventions)


@app.route('/invention/<domain_key>/<invention_id>')
def view_invention(domain_key, invention_id):
    """View a specific invention"""
    domain_info = get_domain_info(domain_key)
    
    try:
        invention = get_invention(domain_key, invention_id)
    except Exception as e:
        flash(f'Error loading invention: {str(e)}', 'error')
        return redirect(url_for('view_domain', domain_key=domain_key))
    
    if not invention:
        flash('Invention not found', 'error')
        return redirect(url_for('view_domain', domain_key=domain_key))
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(invention['content'], extras=['fenced-code-blocks', 'tables'])
    
    return render_template('invention.html',
                         domain_key=domain_key,
                         domain_info=domain_info,
                         invention=invention,
                         html_content=html_content)


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Generate a new invention"""
    if request.method == 'POST':
        domain_key = request.form.get('domain')
        domain_info = get_domain_info(domain_key)
        
        if not domain_info:
            flash('Invalid domain selected', 'error')
            return redirect(url_for('generate'))
        
        try:
            inv_id = generate_invention(domain_key, domain_info['name'])
            flash(f'Successfully generated invention: {inv_id}', 'success')
            return redirect(url_for('view_invention', domain_key=domain_key, invention_id=inv_id))
        except Exception as e:
            flash(f'Error generating invention: {str(e)}', 'error')
            return redirect(url_for('generate'))
    
    return render_template('generate.html', domains=DOMAINS)


@app.route('/search')
def search():
    """Search across all inventions"""
    query = request.args.get('q', '')
    if not query:
        return render_template('search.html', query='', results=[])
    
    try:
        raw_results = db_search_inventions(query)
        # Format results to match template expectations
        results = []
        for result in raw_results:
            # Find context around match
            content = result.get('content', '')
            content_lower = content.lower()
            query_lower = query.lower()
            match_pos = content_lower.find(query_lower)
            if match_pos >= 0:
                start = max(0, match_pos - 100)
                end = min(len(content), match_pos + 100)
                context = ('...' if start > 0 else '') + content[start:end] + ('...' if end < len(content) else '')
            else:
                context = content[:200] + '...'
            
            results.append({
                'domain_key': result['domain_key'],
                'domain_name': result['domain_name'],
                'id': result['invention_id'],
                'title': result['title'],
                'context': context,
                'date': result['created_at']
            })
    except Exception as e:
        flash(f'Error searching: {str(e)}', 'error')
        results = []
    
    return render_template('search.html', query=query, results=results)


@app.route('/stats')
def stats():
    """Statistics dashboard"""
    try:
        stats_data = get_stats()
        # Get recent inventions
        recent_inventions = get_all_inventions(limit=20)
        stats_data['recent_inventions'] = recent_inventions
    except Exception as e:
        flash(f'Error loading statistics: {str(e)}', 'error')
        stats_data = {'total_inventions': 0, 'domains_active': 0, 'by_domain': {}, 'recent_inventions': []}
    
    return render_template('stats.html', stats=stats_data, domains=DOMAINS)


# Helper functions (kept for backward compatibility and template formatting)


if __name__ == '__main__':
    app.run(debug=True)

