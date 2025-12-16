# Auto-Generation Feature

The Perpetual Ideas Machine can automatically generate inventions in the background at regular intervals.

## Configuration

Add these settings to your `.env` file:

```bash
# Enable/disable auto-generation
AUTO_GENERATE=true

# Interval in seconds (default: 3600 = 1 hour)
AUTO_GENERATE_INTERVAL=3600
```

## ⏰ Auto-Generation Schedule

- **Interval**: Every 1 hour (3600 seconds) by default
- **Cutoff Date**: February 1, 2026
- **Automatic Shutdown**: The scheduler will automatically stop after the cutoff date

The app will display how many days remain until the cutoff when it starts:
```
🤖 Auto-generation enabled: every 3600 seconds (60.0 minutes)
📅 Will run until February 1, 2026 (46 days remaining)
```

## How It Works

1. **Background Scheduler**: Uses APScheduler to run generation tasks in the background
2. **Random Domain Selection**: Each auto-generation picks a random technology domain
3. **Date Check**: Before each generation, checks if we're past February 1, 2026
4. **Automatic Shutdown**: Stops generating after the cutoff date
5. **Independent of Web UI**: Auto-generation happens even when no one is using the website

## Interval Examples

```bash
AUTO_GENERATE_INTERVAL=60     # 1 minute (fast - good for testing)
AUTO_GENERATE_INTERVAL=300    # 5 minutes
AUTO_GENERATE_INTERVAL=600    # 10 minutes
AUTO_GENERATE_INTERVAL=1800   # 30 minutes
AUTO_GENERATE_INTERVAL=3600   # 1 hour (default)
AUTO_GENERATE_INTERVAL=7200   # 2 hours
AUTO_GENERATE_INTERVAL=86400  # 24 hours (1 day)
```

## Disabling Auto-Generation

Set to `false` in `.env`:

```bash
AUTO_GENERATE=false
```

Or remove the line entirely.

## Monitoring Auto-Generation

Check your Flask app logs to see auto-generation activity:

```bash
# Startup message:
🤖 Auto-generation enabled: every 3600 seconds (60.0 minutes)
📅 Will run until February 1, 2026 (46 days remaining)

# Successful generations:
✅ Auto-generated invention inv-20251216-182030 in Mechanical Engineering
✅ Auto-generated invention inv-20251216-192030 in Materials Science

# When cutoff date is reached:
⏹️  Auto-generation stopped: Reached cutoff date (Feb 1, 2026)

# If already past cutoff on startup:
⏹️  Auto-generation disabled: Past cutoff date (Feb 1, 2026)
```

## Use Cases

### Research & Testing
- **Fast intervals (1-5 minutes)**: Quickly build up a corpus of AI-generated inventions
- Monitor what AI generates across different domains

### Production Prior Art Service
- **Moderate intervals (10-30 minutes)**: Steady stream of prior art publications
- Maintain an active, growing database

### Background Operation
- **Slow intervals (1-6 hours)**: Occasional automated contributions
- Supplement manual generations

## Cost Considerations

Each auto-generated invention costs:
- **OpenAI GPT-4**: ~$0.03-0.06 per invention
- **Anthropic Claude**: ~$0.02-0.04 per invention

**Examples (until Feb 1, 2026):**
- 5-minute intervals = 288 inventions/day ≈ $8-17/day
- 30-minute intervals = 48 inventions/day ≈ $1.50-3/day
- 1-hour intervals (default) = 24 inventions/day ≈ $0.50-1.50/day
- 2-hour intervals = 12 inventions/day ≈ $0.25-0.75/day

**Note:** Auto-generation will automatically stop on February 1, 2026 to cap total costs.
- 6-hour intervals = 4 inventions/day ≈ $0.10-0.25/day

## Heroku Deployment

Auto-generation works on Heroku! Just set the environment variables:

```bash
heroku config:set AUTO_GENERATE=true
heroku config:set AUTO_GENERATE_INTERVAL=300
```

**Note**: Heroku free/hobby dynos sleep after 30 minutes of inactivity. Upgrade to a standard dyno or higher to keep auto-generation running continuously.

## Technical Details

- **Scheduler**: APScheduler BackgroundScheduler
- **Thread-safe**: Safe to run alongside web requests
- **Graceful shutdown**: Scheduler stops cleanly when app exits
- **Error handling**: Failed generations are logged but don't stop the scheduler

## Logs

Auto-generation events are logged to stdout:

```bash
# Start message
🤖 Auto-generation enabled: every 300 seconds (5.0 minutes)

# Success
✅ Auto-generated invention inv-20251216-182030 in Biotechnology

# Error
❌ Auto-generation error: OPENAI_API_KEY not set in environment
```

## Tips

1. **Start slow**: Begin with 10-30 minute intervals to monitor behavior
2. **Watch costs**: Check your API usage on OpenAI/Anthropic dashboard
3. **Monitor storage**: Each invention is ~2-5KB of text
4. **Commit regularly**: Use git to track all generated inventions
5. **Set alerts**: Monitor your deployment logs for errors

## Stopping Auto-Generation

### During Development
- Stop the Flask app (Ctrl+C)
- The scheduler will shut down cleanly

### On Heroku
```bash
# Disable without redeploying
heroku config:set AUTO_GENERATE=false

# Or restart the app to reload settings
heroku restart
```

## Future Enhancements

Possible improvements:
- Web UI to enable/disable auto-generation
- Rate limiting per domain
- Scheduled times (e.g., only during business hours)
- Webhooks to notify when inventions are generated
- Analytics dashboard for auto-generated inventions

---

**Happy auto-generating! 🤖**

