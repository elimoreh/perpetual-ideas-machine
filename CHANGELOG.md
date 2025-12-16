# Changelog - Perpetual Ideas Machine

## 2025-12-16 - Major Update: Enhanced Quality + PostgreSQL

### 🎯 Feature: Enhanced AI Prompting for Higher Quality Inventions

**Problem:** Original prompts generated obvious technology combinations that wouldn't qualify as truly novel inventions (e.g., "drone + AI + camera").

**Solution:** Completely redesigned prompts with:
- Explicit anti-obviousness instructions
- Requirements for specific technical details (materials, dimensions, formulas)
- Counter-intuitive problem-solving focus
- Enhanced enablement requirements
- Increased AI creativity (temperature 1.0, max_tokens 3000)

**Impact:** Inventions are now much more detailed, technically specific, and truly novel.

**Files Modified:**
- `generate.py` - Enhanced prompts for both OpenAI and Anthropic

---

### 🗄️ Feature: PostgreSQL Database Migration (Heroku-Ready)

**Problem:** Heroku's ephemeral filesystem loses all file-based data on dyno restart (happens daily), making the file-based storage unsuitable for production.

**Solution:** Migrated to PostgreSQL database for persistent, scalable storage.

**Impact:** 
- ✅ Works on Heroku production environment
- ✅ Data persists across restarts and deployments
- ✅ Scalable to millions of inventions
- ✅ Built-in backup/restore capabilities

**New Files:**
- `database.py` - PostgreSQL database management
- `init_db.py` - Database initialization script
- `DATABASE_SETUP.md` - Comprehensive PostgreSQL setup guide
- `MIGRATION_SUMMARY.md` - Migration technical details
- `IMPROVEMENTS.md` - Overview of both improvements

**Modified Files:**
- `generate.py` - Save to PostgreSQL instead of files
- `app.py` - Read from PostgreSQL, removed file-based helpers
- `requirements.txt` - Added `psycopg2-binary==2.9.9`
- `env.example` - Added DATABASE_URL configuration
- `DEPLOYMENT.md` - Added PostgreSQL setup instructions
- `START_HERE.md` - Updated prerequisites and setup steps

**New Requirements:**
- PostgreSQL 15+ for local development
- Heroku Postgres add-on for production ($5/month)
- DATABASE_URL environment variable

**Database Schema:**
```sql
CREATE TABLE inventions (
    id SERIAL PRIMARY KEY,
    invention_id VARCHAR(255) UNIQUE NOT NULL,
    domain_key VARCHAR(255) NOT NULL,
    domain_name VARCHAR(255) NOT NULL,
    title TEXT,
    content TEXT NOT NULL,
    hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Quick Upgrade Guide

### For Existing Users

```bash
# 1. Install PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# 2. Create database
createdb pim_db

# 3. Update dependencies
pip install -r requirements.txt

# 4. Add DATABASE_URL to .env
echo "DATABASE_URL=postgresql://localhost:5432/pim_db" >> .env

# 5. Initialize database
python init_db.py

# 6. Run app (existing file-based inventions won't be migrated)
python app.py
```

### For Heroku Deployment

```bash
# Add PostgreSQL addon
heroku addons:create heroku-postgresql:essential-0

# Deploy
git add .
git commit -m "Upgrade to PostgreSQL and enhanced prompts"
git push heroku main
```

---

## Breaking Changes

⚠️ **File-based storage no longer supported**
- Existing inventions in `publications/` directory will not be automatically loaded
- Option 1: Create migration script (see DATABASE_SETUP.md)
- Option 2: Generate new inventions (recommended)

⚠️ **New dependencies required**
- PostgreSQL database server
- psycopg2-binary Python package

---

## Cost Changes

**Before:** $5-7/month (Heroku dyno only)
**After:** $10-12/month (dyno + PostgreSQL)

**Breakdown:**
- Heroku Eco Dyno: $5/month
- Heroku Postgres Essential-0: $5/month
- OpenAI API: ~$0.03-0.06 per invention

---

## Documentation Updates

New documentation files:
- `DATABASE_SETUP.md` - PostgreSQL setup and troubleshooting
- `MIGRATION_SUMMARY.md` - Technical migration details
- `IMPROVEMENTS.md` - Overview of improvements
- `CHANGELOG.md` - This file

Updated documentation:
- `START_HERE.md` - Added PostgreSQL prerequisites
- `DEPLOYMENT.md` - Added PostgreSQL deployment steps
- `env.example` - Added DATABASE_URL

---

## Testing Checklist

After upgrading, verify:
- [ ] PostgreSQL installed and running
- [ ] Database created (`createdb pim_db`)
- [ ] DATABASE_URL set in `.env`
- [ ] Database initialized (`python init_db.py`)
- [ ] App starts without errors
- [ ] Can generate inventions
- [ ] Inventions are higher quality and more detailed
- [ ] Can view inventions
- [ ] Search works
- [ ] Statistics page works
- [ ] Inventions persist after app restart

---

## Rollback Instructions

If you need to rollback:

```bash
# Revert to previous version
git log --oneline  # Find commit hash before migration
git revert <commit-hash>

# Or checkout previous version
git checkout <commit-hash-before-migration>
```

Note: You'll lose PostgreSQL-stored inventions unless you export them first.

---

## Support

For help with:
- **PostgreSQL setup:** See `DATABASE_SETUP.md`
- **Heroku deployment:** See `DEPLOYMENT.md`
- **General setup:** See `START_HERE.md`

---

## What's Next?

Potential future improvements:
- [ ] Migration script for existing file-based inventions
- [ ] Full-text search with PostgreSQL tsvector
- [ ] Invention categories and tags
- [ ] User accounts and favorites
- [ ] API endpoints for programmatic access
- [ ] Export inventions as PDF
- [ ] Invention comparison tools

---

**Version:** 2.0.0 (PostgreSQL + Enhanced Prompting)  
**Date:** 2025-12-16  
**Status:** Production Ready ✅

