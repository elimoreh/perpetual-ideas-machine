# Heroku Deployment Guide

Complete guide for deploying Perpetual Ideas Machine to Heroku.

## Prerequisites

- [Heroku account](https://signup.heroku.com/)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- Git installed
- OpenAI or Anthropic API key

## Installation

### 1. Install Heroku CLI

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Windows:**
Download from https://devcenter.heroku.com/articles/heroku-cli

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### 2. Login to Heroku

```bash
heroku login
```

This will open a browser for authentication.

## Deployment Steps

### 1. Initialize Git Repository

```bash
cd /path/to/perpetual-ideas-machine
git init
git add .
git commit -m "Initial commit: Perpetual Ideas Machine"
```

### 2. Create Heroku App

```bash
heroku create perpetual-ideas-machine
# Or with a custom name:
heroku create your-custom-name
```

This creates a new Heroku app and adds a git remote.

### 3. Add PostgreSQL Database

```bash
# Add Heroku Postgres (Essential-0 plan: $5/month)
heroku addons:create heroku-postgresql:essential-0

# Wait for database to be ready
heroku pg:wait

# Verify DATABASE_URL was set automatically
heroku config:get DATABASE_URL
```

**Note:** The database will be automatically initialized when the app starts.

### 4. Set Environment Variables

```bash
# Required: OpenAI API Key
heroku config:set OPENAI_API_KEY=sk-your-actual-openai-key

# Required: Flask Secret Key
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Optional: AI Provider (default is openai)
heroku config:set AI_PROVIDER=openai

# Optional: If using Anthropic instead
# heroku config:set ANTHROPIC_API_KEY=sk-ant-your-key
# heroku config:set AI_PROVIDER=anthropic
```

### 5. Deploy to Heroku

```bash
git push heroku main
```

Wait for the build to complete (2-3 minutes).

### 6. Open Your App

```bash
heroku open
```

Your app is now live! 🎉

### 7. Verify Database

```bash
# Check database status
heroku pg:info

# View inventions (after generating some)
heroku pg:psql
SELECT COUNT(*) FROM inventions;
\q
```

## Verifying Deployment

### Check Logs

```bash
heroku logs --tail
```

### Check App Status

```bash
heroku ps
```

Should show:
```
web.1: up 2025/12/16 12:00:00 (~ 1m ago)
```

### Test the App

Visit your app URL and try:
1. Homepage loads correctly
2. Domain pages are accessible
3. Generate a test invention
4. Search functionality works

## Managing Your Deployment

### View Configuration

```bash
heroku config
```

### Update Environment Variables

```bash
heroku config:set VARIABLE_NAME=new-value
```

### Restart the App

```bash
heroku restart
```

### View Recent Logs

```bash
heroku logs -n 200
```

### Access Heroku Dashboard

```bash
heroku dashboard
```

## Updating Your App

After making changes:

```bash
git add .
git commit -m "Description of changes"
git push heroku main
```

## Custom Domain (Optional)

### Add a Custom Domain

```bash
heroku domains:add www.yourdomain.com
```

### Configure DNS

Add a CNAME record:
```
CNAME: www.yourdomain.com → your-app-name.herokuapp.com
```

## Cost Considerations

### Heroku Costs

**Eco Dynos** ($5/month per dyno)
- 1000 dyno hours per month
- Sleeps after 30 minutes of inactivity
- Good for prototypes and demos

**Hobby Plan** ($7/month)
- Never sleeps
- Better for production use

**PostgreSQL Database** ($5/month minimum)
- Essential-0: $5/month (10,000 rows, 1 GB storage)
- Essential-1: $50/month (10M rows, 64 GB storage)
- See [DATABASE_SETUP.md](DATABASE_SETUP.md) for details

### API Costs

- **OpenAI GPT-4:** ~$0.03-0.06 per invention
- **Anthropic Claude:** ~$0.02-0.04 per invention

**Total Monthly Cost Examples:**
- **Light Usage:** ~$15/month ($5 dyno + $5 database + $5 API)
- **Moderate Usage:** ~$20-30/month (100-200 inventions)
- **Heavy Usage:** ~$50-100/month (1000+ inventions)

## Troubleshooting

### App Crashes on Start

```bash
heroku logs --tail
```

Common issues:
- Missing environment variables
- Invalid API keys
- Dependency conflicts

### "No web processes running"

```bash
heroku ps:scale web=1
```

### Port Binding Error

Make sure `app.py` uses:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### Out of Memory

Upgrade dyno type:
```bash
heroku ps:resize web=standard-1x
```

## Monitoring

### Set Up Alerts

```bash
heroku addons:create papertrail
```

### View Metrics

```bash
heroku dashboard
```

Go to Metrics tab to see:
- Response times
- Throughput
- Memory usage
- Error rates

## Backup Strategy

### Backup PostgreSQL Database

```bash
# Create a backup
heroku pg:backups:capture

# Download the backup
heroku pg:backups:download

# List all backups
heroku pg:backups
```

### Restore from Backup

```bash
# Restore to Heroku (⚠️  overwrites current data)
heroku pg:backups:restore [BACKUP_ID] DATABASE_URL

# Restore to local PostgreSQL
pg_restore --verbose --clean --no-acl --no-owner -h localhost -d pim_db latest.dump
```

### Automated Backups

Heroku Postgres Essential plans include:
- Daily automatic backups
- 7-day retention for Essential-0
- Longer retention for higher plans

See [DATABASE_SETUP.md](DATABASE_SETUP.md) for more details.

## Scaling

### Increase Dynos

```bash
heroku ps:scale web=2
```

### Upgrade Dyno Type

```bash
heroku ps:resize web=standard-2x
```

## Security

### Rotate API Keys

```bash
# Get new key from OpenAI
heroku config:set OPENAI_API_KEY=new-key
heroku restart
```

### Enable HTTPS

Heroku provides free SSL:
- Automatic for `*.herokuapp.com`
- Automatic for custom domains on Hobby tier+

## Uninstalling

```bash
heroku apps:destroy your-app-name
```

## Support

- [Heroku Documentation](https://devcenter.heroku.com/)
- [Heroku Status](https://status.heroku.com/)
- [Heroku Support](https://help.heroku.com/)

## Next Steps

1. ✅ Deploy app
2. ✅ Generate test inventions
3. Set up monitoring
4. Configure custom domain
5. Set up automated backups
6. Share with users!

---

Happy deploying! 🚀

