# PostgreSQL Database Setup

The Perpetual Ideas Machine now uses PostgreSQL instead of file-based storage, making it fully compatible with Heroku's ephemeral filesystem.

## Why PostgreSQL?

Heroku's filesystem is **ephemeral** - any files written to disk are lost when:
- The dyno restarts (at least once per day)
- The application is deployed
- The dyno crashes or is restarted

PostgreSQL ensures your inventions are permanently stored.

## Local Development Setup

### Option 1: PostgreSQL Locally (Recommended for Production-like Testing)

1. **Install PostgreSQL**
   ```bash
   # macOS
   brew install postgresql@15
   brew services start postgresql@15
   
   # Ubuntu/Debian
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   
   # Windows
   # Download from https://www.postgresql.org/download/windows/
   ```

2. **Create Database**
   ```bash
   # Create database
   createdb pim_db
   
   # Or using psql:
   psql postgres
   CREATE DATABASE pim_db;
   \q
   ```

3. **Set DATABASE_URL in .env**
   ```bash
   DATABASE_URL=postgresql://your_username@localhost:5432/pim_db
   
   # If you set a password:
   DATABASE_URL=postgresql://your_username:your_password@localhost:5432/pim_db
   ```

4. **Initialize Database**
   ```bash
   python init_db.py
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

### Option 2: Quick Testing (Not Recommended for Heroku Deploy)

If you just want to test locally without PostgreSQL, you can use SQLite temporarily, but **this won't work on Heroku**.

## Heroku Deployment Setup

### 1. Add Heroku Postgres

```bash
# Add PostgreSQL to your Heroku app
heroku addons:create heroku-postgresql:essential-0

# This automatically sets the DATABASE_URL environment variable
# Check it was set:
heroku config:get DATABASE_URL
```

The `essential-0` plan is **$5/month** and includes:
- 10,000 rows
- 1 GB storage
- 20 connections

For higher usage, consider:
- `essential-1`: $50/month (10M rows, 64 GB)
- `essential-2`: $200/month (125M rows, 256 GB)

### 2. Initialize Database on Heroku

The database will be automatically initialized when the app starts (in `app.py`), but you can also manually initialize:

```bash
heroku run python init_db.py
```

### 3. Deploy

```bash
git add .
git commit -m "Add PostgreSQL support"
git push heroku main
```

### 4. Verify

```bash
# Check logs
heroku logs --tail

# Open app
heroku open
```

## Database Schema

The database has one main table:

```sql
CREATE TABLE inventions (
    id SERIAL PRIMARY KEY,
    invention_id VARCHAR(255) UNIQUE NOT NULL,
    domain_key VARCHAR(255) NOT NULL,
    domain_name VARCHAR(255) NOT NULL,
    title TEXT,
    content TEXT NOT NULL,
    hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_domain_key ON inventions(domain_key);
CREATE INDEX idx_created_at ON inventions(created_at);
CREATE INDEX idx_invention_id ON inventions(invention_id);
```

## Database Management

### View Database Contents

```bash
# Locally
psql pim_db
SELECT COUNT(*) FROM inventions;
SELECT invention_id, domain_key, created_at FROM inventions ORDER BY created_at DESC LIMIT 10;

# On Heroku
heroku pg:psql
SELECT COUNT(*) FROM inventions;
```

### Backup Database

```bash
# Heroku backup
heroku pg:backups:capture
heroku pg:backups:download

# This downloads latest.dump
# Restore with:
pg_restore --verbose --clean --no-acl --no-owner -h localhost -d pim_db latest.dump
```

### Reset Database

```bash
# Locally
dropdb pim_db
createdb pim_db
python init_db.py

# On Heroku (⚠️  CAUTION: Deletes all data!)
heroku pg:reset DATABASE_URL
heroku run python init_db.py
```

## Troubleshooting

### "DATABASE_URL not set"

Add DATABASE_URL to your `.env` file:
```bash
DATABASE_URL=postgresql://localhost:5432/pim_db
```

### "could not connect to server"

Make sure PostgreSQL is running:
```bash
# macOS
brew services start postgresql@15

# Linux
sudo systemctl start postgresql
```

### "permission denied for schema public"

Grant permissions:
```bash
psql pim_db
GRANT ALL ON SCHEMA public TO your_username;
```

### Heroku: "no pg:credentials"

Make sure you've added the Postgres add-on:
```bash
heroku addons:create heroku-postgresql:essential-0
```

### Connection Pool Exhausted

If you get "connection pool exhausted" errors, you may need to:
1. Upgrade your Heroku Postgres plan (more connections)
2. Add connection pooling (PgBouncer)

```bash
# Add PgBouncer
heroku addons:create heroku-postgresql:essential-0
heroku pg:wait
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-pgbouncer
```

## Migration from File-Based Storage

If you have existing inventions in the `publications/` directory:

1. **Create a migration script** (optional):
   ```python
   # migrate_to_db.py
   import os
   import glob
   from database import save_invention
   
   for md_file in glob.glob('publications/**/*.md', recursive=True):
       with open(md_file, 'r') as f:
           content = f.read()
       
       # Extract metadata from filename/path
       parts = md_file.split('/')
       domain_key = parts[1]
       invention_id = os.path.basename(md_file).replace('.md', '')
       
       # Parse content for title, etc.
       # ... (implement parsing logic)
       
       save_invention(invention_id, domain_key, domain_name, title, content, hash_value)
   ```

2. **Or simply regenerate inventions** - since they're AI-generated, you can just generate new ones.

## Cost Estimate

### Local Development
- **Free** (just PostgreSQL on your machine)

### Heroku Production
- **Essential-0 Plan**: $5/month
  - Good for: 10,000+ inventions
  - 1 GB storage
  - 20 concurrent connections
  
- **Essential-1 Plan**: $50/month (if you need more)
  - 10 million rows
  - 64 GB storage
  - Better performance

## Next Steps

1. ✅ Install PostgreSQL locally
2. ✅ Create database and set DATABASE_URL
3. ✅ Run `python init_db.py`
4. ✅ Test locally with `python app.py`
5. ✅ Add Heroku Postgres add-on
6. ✅ Deploy to Heroku

---

**Your inventions are now persistent and Heroku-ready! 🚀**

