import json
import os
from typing import Any

import streamlit as st
from groq import Groq


DEFAULT_REPORT = {
    "scientific_name": "Not available",
    "description": "No description available.",
    "treatment_steps": [],
    "recommended_fertilizers": [],
    "tips_for_improvement": [],
    "comparison_with_healthy_leaf": "No comparison available.",
}

DEFAULT_GROQ_API_KEY = ""


def generate_fallback_report(
    disease_name: str,
    confidence: float,
    plant_name: str = "Unknown Plant",
    model_outputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a local structured report when Groq is unavailable."""
    confidence_note = "high" if confidence >= 85 else "moderate" if confidence >= 60 else "low"
    top_predictions = (model_outputs or {}).get("top_predictions", [])
    alternatives = [
        f"{item.get('plant_name', 'Unknown Plant')} - {item.get('disease_name', 'Unknown')} ({item.get('confidence', 0)}%)"
        for item in top_predictions[1:4]
    ]

    if disease_name.lower() == "healthy":
        description = (
            f"The model identified the uploaded image as a healthy {plant_name} leaf with "
            f"{confidence:.2f}% confidence. This suggests no obvious disease pattern was detected, "
            "but regular visual inspection is still recommended."
        )
        treatment_steps = [
            "Continue regular monitoring for spots, curling, yellowing, or mold.",
            "Water at the soil level and avoid wetting leaves for long periods.",
            "Remove dead or damaged leaves to reduce pest and pathogen pressure.",
            "Maintain good airflow and adequate spacing between plants.",
        ]
    else:
        description = (
            f"The model predicts {disease_name} on {plant_name} with {confidence:.2f}% confidence, "
            f"which is a {confidence_note}-confidence result. Confirm symptoms visually before applying treatment."
        )
        if alternatives:
            description += " Similar model alternatives include: " + "; ".join(alternatives) + "."
        treatment_steps = [
            "Isolate the affected plant if possible to reduce spread.",
            "Remove and discard heavily infected leaves; do not compost diseased material.",
            "Sanitize pruning tools after use.",
            "Improve airflow around the plant and avoid overhead watering.",
            "Use an appropriate organic or approved fungicide/bactericide if symptoms match the prediction.",
        ]

    return normalize_report(
        {
            "scientific_name": "Confirm with local agricultural extension or plant pathology lab",
            "description": description,
            "treatment_steps": treatment_steps,
            "recommended_fertilizers": [
                "Balanced NPK fertilizer based on crop stage",
                "Organic compost to improve soil structure",
                "Potassium-rich nutrients to support stress tolerance",
                "Micronutrient mix only if deficiency symptoms or soil test indicate need",
            ],
            "tips_for_improvement": [
                "Upload a clear close-up image of one leaf in natural light.",
                "Capture both upper and lower leaf surfaces when symptoms are visible.",
                "Avoid blurry images, harsh shadows, and cluttered backgrounds.",
                "Compare the result with visible symptoms before treatment.",
                "Repeat prediction with another leaf if confidence is low or symptoms vary.",
            ],
            "comparison_with_healthy_leaf": (
                "A healthy leaf usually has even green color, firm texture, and no spreading spots, lesions, "
                "powdery growth, curling, or yellowing. A diseased leaf may show irregular discoloration, "
                "brown or black lesions, wilted areas, mold-like patches, or reduced vigor."
            ),
        }
    )


def get_groq_api_key() -> str | None:
    """Read Groq API key from Streamlit secrets or environment variables."""
    try:
        return st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") or DEFAULT_GROQ_API_KEY
    except Exception:
        return os.getenv("GROQ_API_KEY") or DEFAULT_GROQ_API_KEY


def extract_json(text: str) -> dict[str, Any]:
    """Parse a JSON object from the model response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end <= start:
            raise ValueError("Groq response did not contain valid JSON.")
        return json.loads(text[start:end])


def normalize_report(report: dict[str, Any]) -> dict[str, Any]:
    """Ensure all expected report keys exist with stable value shapes."""
    normalized = DEFAULT_REPORT.copy()
    normalized.update(report or {})

    list_keys = ["treatment_steps", "recommended_fertilizers", "tips_for_improvement"]
    for key in list_keys:
        value = normalized.get(key)
        if isinstance(value, str):
            normalized[key] = [value]
        elif not isinstance(value, list):
            normalized[key] = []

    return normalized


def generate_report(
    disease_name: str,
    confidence: float,
    plant_name: str = "Unknown Plant",
    model_outputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate a structured plant disease report using the Groq API."""
    api_key = get_groq_api_key()
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to Streamlit secrets or environment variables.")

    client = Groq(api_key=api_key)

    system_prompt = """
You are an expert plant pathologist and agronomy assistant for a plant disease detection web app.
Your job is to turn an AI model prediction into a useful, cautious, farmer-friendly report.

Rules:
- Return only one valid JSON object. Do not include markdown, headings, code fences, or extra text.
- Use the predicted plant name, disease name, raw model label, top predictions, and model confidence as context, but do not claim the diagnosis is certain.
- If confidence is 85% or higher, write with strong but still cautious wording.
- If confidence is 60% to 84%, mention that visual symptoms should be checked before treatment.
- If confidence is below 60%, clearly say the prediction is uncertain and recommend expert/lab confirmation.
- If top predictions are close in confidence, mention that similar diseases may need visual confirmation.
- Give practical, generalized fertilizer recommendations. Do not invent exact brand names or unsafe chemical doses.
- Treatment steps must be actionable and safe: isolate if needed, prune/remove infected leaves, improve airflow, avoid overhead watering, sanitize tools, and use suitable organic or approved fungicide/bactericide guidance when relevant.
- Tips for improvement should be based on the confidence level, image quality, disease severity cues, and healthy crop management.
- The healthy-leaf comparison must describe visible differences such as color, spots, lesions, curling, mold, wilting, texture, and overall vigor.
- Keep each field concise but informative.

Required JSON schema:
{
  "scientific_name": "scientific name of the disease, pathogen, or causal organism when known",
  "description": "2-4 sentence explanation of the disease and what the confidence means",
  "treatment_steps": ["4-6 clear treatment actions"],
  "recommended_fertilizers": ["3-5 generalized fertilizer or soil amendment suggestions"],
  "tips_for_improvement": ["4-6 practical improvement or prevention tips"],
  "comparison_with_healthy_leaf": "3-5 sentence comparison between the detected condition and a healthy leaf"
}
"""

    user_prompt = f"""
Prediction result:
- Plant name: {plant_name}
- Disease name: {disease_name}
- Model confidence: {confidence:.2f}%
- Full model output JSON:
{json.dumps(model_outputs or {}, indent=2)}

Generate the structured plant health report now.
"""

    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.25,
            max_tokens=900,
            response_format={"type": "json_object"},
        )
    except Exception:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.25,
            max_tokens=900,
        )

    content = response.choices[0].message.content or "{}"
    return normalize_report(extract_json(content))
