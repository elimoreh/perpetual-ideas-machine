# Perpetual Ideas Machine

> Using AI to preserve the patent commons by generating and publishing prior art at scale

## Overview

The Perpetual Ideas Machine is an AI-powered system that generates novel, technically detailed inventions and immediately publishes them as prior art. By creating a continuous stream of publicly available technical disclosures, we aim to:

- **Prevent Patent Trolling:** Make it harder for patent trolls to file broad patents on AI-generated outputs
- **Preserve the Commons:** Keep innovative ideas in the public domain where they can benefit everyone
- **Document AI Capabilities:** Create a timestamped record of what AI systems can generate
- **Enable Innovation:** Provide a searchable database of technical concepts for researchers and inventors

All inventions are published under **CC0 1.0 Universal** (Public Domain Dedication).

## Features

- ✨ **AI-Powered Generation:** Uses OpenAI or Anthropic APIs to generate detailed, novel inventions
- 📚 **10 Technology Domains:** Covers mechanical engineering, materials science, biotech, software, and more
- 🔍 **Full-Text Search:** Search across all published inventions
- 📊 **Statistics Dashboard:** Track generation activity and browse by domain
- 🔐 **Cryptographic Verification:** Each invention includes SHA-256 hash and timestamp
- 📝 **Structured Format:** Publications include title, abstract, detailed description, claims, and enablement
- 🌐 **Web Interface:** Beautiful, responsive UI built with Flask and Bootstrap

## Technology Domains

1. ⚙️ Mechanical Engineering
2. 🔬 Materials Science
3. 🧪 Chemical Engineering
4. 💊 Pharmaceutical Chemistry
5. ⚡ Electrical Engineering
6. 💻 Software Algorithms
7. 🧬 Biotechnology
8. 🌱 Environmental Technology
9. 🏥 Medical Devices
10. 🌾 Agricultural Technology

## Setup

### Prerequisites

- Python 3.11.6+
- OpenAI API key or Anthropic API key
- Git (for deployment)

### Local Development

1. **Clone or create the project:**

```bash
cd perpetual-ideas-machine
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

```bash
cp env.example .env
```

Edit `.env` and add your API keys:

```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here

SECRET_KEY=your-random-secret-key-here
AI_PROVIDER=openai  # or "anthropic"
```

5. **Run the application:**

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Deployment to Heroku

### Prerequisites

- Heroku account ([signup here](https://signup.heroku.com/))
- Heroku CLI installed ([installation guide](https://devcenter.heroku.com/articles/heroku-cli))

### Deployment Steps

1. **Login to Heroku:**

```bash
heroku login
```

2. **Create a new Heroku app:**

```bash
heroku create your-app-name
```

3. **Set environment variables:**

```bash
heroku config:set OPENAI_API_KEY=sk-your-openai-api-key-here
heroku config:set SECRET_KEY=your-random-secret-key-here
heroku config:set AI_PROVIDER=openai
```

4. **Initialize git repository (if not already):**

```bash
git init
git add .
git commit -m "Initial commit"
```

5. **Deploy to Heroku:**

```bash
git push heroku main
```

6. **Open your app:**

```bash
heroku open
```

### Managing Your Heroku App

```bash
# View logs
heroku logs --tail

# Restart the app
heroku restart

# Check app status
heroku ps

# Update environment variables
heroku config:set VARIABLE_NAME=value
```

## Project Structure

```
perpetual-ideas-machine/
├── app.py                    # Main Flask application
├── generate.py               # Invention generation logic
├── domains.py                # Domain definitions and metadata
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku process configuration
├── runtime.txt               # Python version specification
├── env.example               # Example environment variables
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── templates/
│   ├── base.html            # Base template with navigation
│   ├── index.html           # Main landing page
│   ├── domain.html          # Domain-specific listing
│   ├── invention.html       # Single invention view
│   ├── generate.html        # Generation form
│   ├── search.html          # Search results
│   └── stats.html           # Statistics dashboard
├── static/
│   └── style.css            # Custom styling
└── publications/
    ├── mechanical-engineering/
    ├── materials-science/
    ├── chemical-engineering/
    ├── pharmaceutical-chemistry/
    ├── electrical-engineering/
    ├── software-algorithms/
    ├── biotechnology/
    ├── environmental-technology/
    ├── medical-devices/
    ├── agricultural-technology/
    └── index.json           # Master index of publications
```

## Usage

### Generating Inventions

1. Navigate to the "Generate" page
2. Select a technology domain
3. Click "Generate Invention"
4. The AI will create a detailed invention and publish it automatically

### Browsing Inventions

- **By Domain:** Click on any domain card on the home page
- **Search:** Use the search bar in the navigation
- **Statistics:** View the stats dashboard for an overview

### Citing as Prior Art

Each invention includes:
- Publication timestamp (ISO 8601 format, UTC)
- Unique identifier
- SHA-256 verification hash
- CC0 1.0 Universal license

These elements provide proof that the disclosure was made public on a specific date, making it valid prior art.

## API Keys

### OpenAI API

1. Sign up at [platform.openai.com](https://platform.openai.com)
2. Generate an API key in your account settings
3. Set as `OPENAI_API_KEY` environment variable

### Anthropic API

1. Sign up at [console.anthropic.com](https://console.anthropic.com)
2. Generate an API key
3. Set as `ANTHROPIC_API_KEY` environment variable
4. Set `AI_PROVIDER=anthropic`

## Legal Notes

### Prior Art Validity

This system publishes inventions as prior art under CC0 1.0 Universal (Public Domain Dedication). Each publication includes:

- Detailed technical description (enablement requirement)
- Timestamp proving public disclosure date
- Cryptographic hash for verification
- Unique identifier for citation

These publications may be cited in patent examinations to demonstrate that an invention was already publicly disclosed.

### License

All generated inventions are dedicated to the public domain under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).

The software itself (this web application) is provided as-is for educational and research purposes.

## Contributing

This is a prototype system. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Disclaimer

This system generates inventions using AI and publishes them as prior art. While these publications may be useful for preventing certain types of patents, they should not be considered legal advice. Consult with a patent attorney for specific legal questions about prior art and patent law.

## Contact

For questions, issues, or suggestions, please open an issue on the project repository.

## Acknowledgments

- Built with Flask, Bootstrap, OpenAI, and Anthropic
- Inspired by the need to preserve the patent commons
- Designed to prevent patent trolling on AI-generated content

---

**Perpetual Ideas Machine** - Keeping innovation in the public domain 🚀

