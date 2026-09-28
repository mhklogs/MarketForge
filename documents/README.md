# MarketForge

AI-powered marketing asset generator — create campaign briefs, ad copies & storyboards using Gemini AI.

## Setup

1. Copy `.env.example` to `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY="your-key-here"
   ```

2. Install dependencies:
   ```bash
   pip install google-genai flask
   ```

3. Run:
   ```bash
   python app.py
   ```

4. Open http://localhost:5000

## Features

- Generate marketing campaign briefs with structured JSON output
- Create localized ad copies for multiple target markets
- Storyboard generation for short-form videos
- Offline-capable PWA (add to home screen)
