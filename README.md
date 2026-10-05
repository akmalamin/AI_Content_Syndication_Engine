# AI Content Syndication Engine (Day 133)

A multi-platform AI content generation engine built with FastAPI and OpenAI GPT.
Generates platform-specific posts (LinkedIn, Twitter, Instagram, Newsletter, Facebook Ads)
from a single topic input with brand voice profiles and character limit enforcement.

## Quick Start
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000