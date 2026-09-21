import json
import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig, GoogleSearch, Tool
from pydantic import BaseModel

MODEL_ID = "gemini-2.5-flash"
_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable not set")
        _client = genai.Client(api_key=api_key)
    return _client

app = Flask(__name__)

class MarketingCampaignBrief(BaseModel):
    campaign_name: str
    campaign_objectives: list[str]
    target_audience: str
    media_strategy: list[str]
    timeline: str
    target_countries: list[str]
    performance_metrics: list[str]

class AdCopy(BaseModel):
    ad_copy_options: list[str]
    localization_notes: list[str]
    visual_description: list[str]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    product_name = data.get("product_name", "")
    description = data.get("description", "")
    target_countries = data.get("target_countries", "")
    timeline = data.get("timeline", "")
    specs = data.get("specs", "")

    product_details = f"""
Product Name: {product_name}
Description: {description}
Target Countries: {target_countries}
Launch Timeline: {timeline}
Tech Specs: {specs}
"""

    try:
        prompt = f"""You are a marketing expert. Create a comprehensive marketing campaign brief for a new product launch.

Product Details:
{product_details}

Return the campaign brief in this JSON structure:
- campaign_name: name of the campaign
- campaign_objectives: list of 3-4 objectives
- target_audience: description of target audience
- media_strategy: list of media channels/strategies
- timeline: campaign timeline
- target_countries: list of target countries
- performance_metrics: list of KPIs"""

        response = get_client().models.generate_content(
            model=MODEL_ID,
            contents=[prompt],
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MarketingCampaignBrief,
            ),
        )
        brief = json.loads(response.text)

        ad_prompt = f"""Given the marketing campaign brief below, create Instagram ad copies localized for each target market.

Campaign Brief:
{response.text}

Return the ad copy in this JSON structure:
- ad_copy_options: list of 3 ad copy variations
- localization_notes: list of localization notes per market
- visual_description: list of visual descriptions per ad"""

        ad_response = get_client().models.generate_content(
            model=MODEL_ID,
            contents=[ad_prompt],
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AdCopy,
            ),
        )
        ad_copy = json.loads(ad_response.text)

        story_prompt = f"""Given the marketing campaign brief below, create a storyboard for a YouTube Shorts video.

Campaign Brief:
{json.dumps(brief)}

Product: {product_name}
Target Countries: {target_countries}

Create a creative storyboard with scenes, timing, visuals, and audio."""

        story_response = get_client().models.generate_content(
            model=MODEL_ID,
            contents=[story_prompt],
        )
        storyboard = story_response.text

        return jsonify({
            "brief": brief,
            "ad_copy": ad_copy,
            "storyboard": storyboard,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
