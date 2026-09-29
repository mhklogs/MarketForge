<div align="center">

# MarketForge

**Product-launch content generator** — feed it a product and it returns a
structured campaign brief, localized ad copy, and a short-form video
storyboard, using Gemini 2.5 Flash with schema-constrained JSON output.

`Python` `Flask` `Gemini 2.5 Flash` `PWA`

</div>

---

## What it does

Most AI marketing demos produce an undifferentiated wall of text. MarketForge
uses **structured output** — every call declares a Pydantic response schema, so
Gemini returns typed JSON rather than prose that has to be regex-scraped.

One request produces three chained assets:

| Stage | Output | Schema enforced |
| --- | --- | --- |
| 1 | Campaign brief — objectives, audience, media strategy, timeline, markets, KPIs | `MarketingCampaignBrief` |
| 2 | Ad copy — three variations per market, with localization notes and visual direction | `AdCopy` |
| 3 | Video storyboard — scenes, timing, visuals, audio for a YouTube Short | Free text |

Stage 2 and 3 both consume stage 1's output, so the three assets stay
narratively consistent instead of being three unrelated generations.

---

## Quickstart

Prerequisites: **Python 3.10+** and a [Gemini API key](https://aistudio.google.com/apikey).

```bash
pip install -r requirements.txt

# set your key
export GEMINI_API_KEY="your-key-here"
# or copy .env.example to .env and source it

python app.py
```

Open <http://localhost:5000>.

| Variable | Required | Description |
| --- | --- | --- |
| `GEMINI_API_KEY` | **Yes** | Gemini API key. Read from the environment at request time |

The model is `gemini-2.5-flash`, set as `MODEL_ID` at the top of `app.py`.
Change it there to swap models.

---

## How the API is shaped

`POST /generate` takes a product profile and returns all three assets at once:

```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Nebula X1",
    "description": "Noise-cancelling over-ear headphones",
    "target_countries": "Japan, Germany, Brazil",
    "timeline": "8 weeks",
    "specs": "40h battery, USB-C, 250g"
  }'
```

Response:

```json
{
  "brief": {
    "campaign_name": "...",
    "campaign_objectives": ["..."],
    "target_audience": "...",
    "media_strategy": ["..."],
    "timeline": "...",
    "target_countries": ["..."],
    "performance_metrics": ["..."]
  },
  "ad_copy": {
    "ad_copy_options": ["..."],
    "localization_notes": ["..."],
    "visual_description": ["..."]
  },
  "storyboard": "..."
}
```

---

## Implementation notes

- **Lazy client initialisation** — the Gemini client is created on first use,
  not at import, so the module imports cleanly without a key present.
- **Structured output** — `GenerateContentConfig(response_schema=...)` with
  `response_mime_type="application/json"` is what makes the schema guarantee
  hold. Pydantic models do the validation.
- **PWA shell** — a service worker and web manifest are included, so the tool
  installs to the home screen.
- **No database** — requests are stateless.

---

## Also in this repo

`creating_marketing_assets_gemini_2_0.ipynb` is the original notebook this
project was built from, kept for reference on how the prompts evolved.

`documents/` holds engineering specs derived from the source tree —
requirements, data-flow diagram, use cases and an architecture summary.

---

## Limitations

- Generated copy is a **starting draft**, not publish-ready creative. It needs a
  human review pass, particularly for claims and localization.
- Storyboard output is free-form text, not schema-enforced.
- Single global API key with no rate limiting or auth on the endpoint. Do not
  expose this to the public as-is.

## License

MIT — use commercially, no attribution required.
