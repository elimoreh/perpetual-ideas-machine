# generate.py
# Invention generation logic using AI

import os
from datetime import datetime
import hashlib
import json
from dotenv import load_dotenv

load_dotenv()

# Check if DATABASE_URL is set to determine which database module to use
database_url = os.getenv('DATABASE_URL')
if database_url:
    from database import save_invention
else:
    from database_sqlite import save_invention

# Determine which AI provider to use
AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai').lower()


def generate_invention(domain_key, domain_name):
    """Generate a novel invention using AI for a specific domain"""
    
    # Check which provider to use
    if AI_PROVIDER == 'anthropic':
        return generate_with_anthropic(domain_key, domain_name)
    else:
        return generate_with_openai(domain_key, domain_name)


def generate_with_openai(domain_key, domain_name):
    """Generate invention using OpenAI API"""
    from openai import OpenAI
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    
    client = OpenAI(api_key=api_key)
    
    prompt = f"""Generate a truly novel and innovative {domain_name} invention that would be worthy of patent protection. This should NOT be:
- A simple combination of existing technologies
- An obvious modification of existing products
- A general improvement without specific technical innovation

Instead, create an invention that:
1. Solves a real problem in a non-obvious way
2. Contains a surprising technical insight or mechanism
3. Has specific, novel technical features (not just "AI-powered" or "smart")
4. Includes concrete specifications (exact materials, dimensions, mechanisms, chemical formulas, algorithms, etc.)
5. Would not be obvious to someone skilled in the {domain_name} field

Think deeply about:
- What fundamental constraints or problems exist in this domain?
- What counter-intuitive approach might work?
- What specific mechanism or structure would enable this?
- What exact parameters or configurations make it work?

Provide in this format:

TITLE: [Specific, descriptive title that captures the core innovation]

ABSTRACT: [2-3 sentences explaining the problem, the non-obvious solution, and key benefit]

DETAILED DESCRIPTION: [Highly specific technical details including:
- Exact materials, alloys, compounds, or technologies (with specifications)
- Precise dimensions, ratios, temperatures, pressures, voltages, etc.
- Detailed structure, mechanism, or algorithm
- How different components interact at a technical level
- Why these specific choices enable the innovation (not just that they do)]

CLAIMS: [List 3-5 specific, technically novel aspects. Each claim should describe something that is:
1. Not obvious from prior art
2. Technically specific (not generic)
3. Essential to the invention's function]

ENABLEMENT: [Step-by-step instructions detailed enough for reproduction, including:
- Specific manufacturing or synthesis procedures
- Testing and calibration methods
- Operating parameters and conditions
- Troubleshooting tips
- Expected performance characteristics]
"""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
        max_tokens=3000
    )
    
    content = response.choices[0].message.content
    
    # Create invention record
    timestamp = datetime.utcnow()
    inv_id = f"inv-{timestamp.strftime('%Y%m%d-%H%M%S')}"
    
    # Extract title
    title = extract_title_from_content(content)
    
    # Format as markdown
    markdown_content = format_invention(content, timestamp, inv_id, domain_key, domain_name)
    
    # Calculate hash
    hash_value = hashlib.sha256(markdown_content.encode()).hexdigest()
    
    # Save to database
    save_invention(inv_id, domain_key, domain_name, title, markdown_content, hash_value)
    
    return inv_id


def generate_with_anthropic(domain_key, domain_name):
    """Generate invention using Anthropic API"""
    import anthropic
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""Generate a truly novel and innovative {domain_name} invention that would be worthy of patent protection. This should NOT be:
- A simple combination of existing technologies
- An obvious modification of existing products
- A general improvement without specific technical innovation

Instead, create an invention that:
1. Solves a real problem in a non-obvious way
2. Contains a surprising technical insight or mechanism
3. Has specific, novel technical features (not just "AI-powered" or "smart")
4. Includes concrete specifications (exact materials, dimensions, mechanisms, chemical formulas, algorithms, etc.)
5. Would not be obvious to someone skilled in the {domain_name} field

Think deeply about:
- What fundamental constraints or problems exist in this domain?
- What counter-intuitive approach might work?
- What specific mechanism or structure would enable this?
- What exact parameters or configurations make it work?

Provide in this format:

TITLE: [Specific, descriptive title that captures the core innovation]

ABSTRACT: [2-3 sentences explaining the problem, the non-obvious solution, and key benefit]

DETAILED DESCRIPTION: [Highly specific technical details including:
- Exact materials, alloys, compounds, or technologies (with specifications)
- Precise dimensions, ratios, temperatures, pressures, voltages, etc.
- Detailed structure, mechanism, or algorithm
- How different components interact at a technical level
- Why these specific choices enable the innovation (not just that they do)]

CLAIMS: [List 3-5 specific, technically novel aspects. Each claim should describe something that is:
1. Not obvious from prior art
2. Technically specific (not generic)
3. Essential to the invention's function]

ENABLEMENT: [Step-by-step instructions detailed enough for reproduction, including:
- Specific manufacturing or synthesis procedures
- Testing and calibration methods
- Operating parameters and conditions
- Troubleshooting tips
- Expected performance characteristics]
"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=3000,
        temperature=1.0,
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = message.content[0].text
    
    # Create invention record
    timestamp = datetime.utcnow()
    inv_id = f"inv-{timestamp.strftime('%Y%m%d-%H%M%S')}"
    
    # Extract title
    title = extract_title_from_content(content)
    
    # Format as markdown
    markdown_content = format_invention(content, timestamp, inv_id, domain_key, domain_name)
    
    # Calculate hash
    hash_value = hashlib.sha256(markdown_content.encode()).hexdigest()
    
    # Save to database
    save_invention(inv_id, domain_key, domain_name, title, markdown_content, hash_value)
    
    return inv_id


def extract_title_from_content(content):
    """Extract title from AI-generated content"""
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith('TITLE:'):
            return line.replace('TITLE:', '').strip()
    return "Untitled Invention"


def format_invention(content, timestamp, inv_id, domain_key, domain_name):
    """Format invention as markdown with metadata"""
    hash_preview = hashlib.sha256(content.encode()).hexdigest()[:16]
    
    markdown = f"""---
title: {inv_id}
domain: {domain_name}
domain_key: {domain_key}
date: {timestamp.isoformat()}Z
id: {inv_id}
hash: sha256:{hash_preview}...
---

# {domain_name} Invention

{content}

---

**Generated by Perpetual Ideas Machine**  
Domain: {domain_name}  
Publication Date: {timestamp.isoformat()}Z  
Verification Hash: sha256:{hash_preview}...

This invention is published as prior art under Creative Commons CC0 1.0 Universal (Public Domain Dedication).
"""
    return markdown

