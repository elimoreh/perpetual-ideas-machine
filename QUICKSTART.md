# Quick Start Guide

Get the Perpetual Ideas Machine running in 5 minutes!

## Step 1: Set Up Environment

Create a `.env` file in the project root:

```bash
# Create .env file
cat > .env << 'EOF'
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=your-secret-key-here
AI_PROVIDER=openai
EOF
```

**Get your OpenAI API key:**
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key and paste it in `.env`

**Generate a secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Step 2: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Install packages
pip install -r requirements.txt
```

## Step 3: Run the App

```bash
python app.py
```

Visit: http://localhost:5000

## Step 4: Generate Your First Invention

1. Click "Generate New Invention"
2. Select a domain (e.g., "Mechanical Engineering")
3. Click "Generate Invention"
4. Wait 10-30 seconds for AI to generate
5. View your published invention!

## Deploy to Heroku (Optional)

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your-key-here
heroku config:set SECRET_KEY=your-secret-here
heroku config:set AI_PROVIDER=openai

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Open app
heroku open
```

## Troubleshooting

### "OPENAI_API_KEY not set"
- Make sure `.env` file exists in project root
- Check that the key is correct (starts with `sk-`)
- Restart the Flask app after changing `.env`

### "No module named 'flask'"
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt`

### "Module 'openai' has no attribute 'OpenAI'"
- Update openai: `pip install --upgrade openai`

### Port already in use
- Change port: `flask run --port 5001`
- Or kill process using port 5000

## Next Steps

- Generate inventions in different domains
- Search for specific technical terms
- View statistics dashboard
- Deploy to Heroku to share with others
- Set up automated generation (cron job)

## Need Help?

Check the full README.md for detailed documentation.

