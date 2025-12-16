# Quick Fix: Get Your App Running Now

## The Issue

The app now requires PostgreSQL database to run (because Heroku's filesystem is ephemeral).
You need to either:
1. Install PostgreSQL locally (recommended)
2. Use a remote PostgreSQL service

## Option 1: Install PostgreSQL Locally (Recommended - 5 minutes)

### Step 1: Install PostgreSQL

```bash
# macOS with Homebrew
brew install postgresql@15
brew services start postgresql@15
```

### Step 2: Create Database

```bash
createdb pim_db
```

### Step 3: Add DATABASE_URL to .env

```bash
cd /Users/elimoreh/Desktop/PIM
echo 'DATABASE_URL=postgresql://localhost:5432/pim_db' >> .env
```

### Step 4: Initialize Database

```bash
source venv/bin/activate
python init_db.py
```

### Step 5: Run App

```bash
python app.py
```

Visit http://localhost:5000 ✅

---

## Option 2: Use Free Remote PostgreSQL (No Local Install)

If you don't want to install PostgreSQL locally, use a free remote database:

### A. ElephantSQL (Free tier available)

1. Go to https://www.elephantsql.com/
2. Sign up for free account
3. Create a new instance (Tiny Turtle plan is free)
4. Copy the connection URL
5. Add to your `.env` file:
   ```bash
   DATABASE_URL=postgres://user:pass@server.elephantsql.com/database
   ```

### B. Neon (Free tier available)

1. Go to https://neon.tech/
2. Sign up for free account
3. Create a new project
4. Copy the connection string
5. Add to your `.env` file:
   ```bash
   DATABASE_URL=postgresql://user:pass@server.neon.tech/database
   ```

### Then:

```bash
source venv/bin/activate
python init_db.py
python app.py
```

---

## Option 3: Just Deploy to Heroku (Skip Local DB)

If you only care about running on Heroku, skip the local database:

```bash
# Create Heroku app
heroku create your-app-name

# Add PostgreSQL (this sets DATABASE_URL automatically)
heroku addons:create heroku-postgresql:essential-0

# Set your API key
heroku config:set OPENAI_API_KEY=sk-your-key-here
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Deploy
git add .
git commit -m "Add PostgreSQL support"
git push heroku main

# Open
heroku open
```

---

## Troubleshooting

### "psycopg2 not found"
Already fixed! ✅ (We just installed it)

### "DATABASE_URL not set"
You need to add DATABASE_URL to your `.env` file. See options above.

### "could not connect to server"
PostgreSQL is not running. Start it:
```bash
brew services start postgresql@15
```

### "database does not exist"
Create the database:
```bash
createdb pim_db
```

---

## What Changed?

Previously: Inventions saved to files in `publications/` folder
- ❌ Lost on Heroku (ephemeral filesystem)

Now: Inventions saved to PostgreSQL database
- ✅ Persists on Heroku
- ✅ Scalable
- ✅ Production-ready

---

## My Recommendation

**For quick testing:** Use Option 2 (ElephantSQL free tier)
**For local development:** Use Option 1 (local PostgreSQL)
**For production:** Use Option 3 (Heroku with Postgres add-on)

Let me know which option you choose and I can help with any issues!

