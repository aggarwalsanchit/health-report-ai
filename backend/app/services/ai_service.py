# app/services/ai_service.py
import os
import google.generativeai as genai
from app.core.config import settings
from app.core.logging import logger

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_report(text: str) -> dict:
    try:
        if not text or len(text.strip()) < 50:
            raise ValueError("Insufficient text for analysis.")

        prompt = f"""
        Analyze the following medical report and return structured JSON with:
        test_name, observed_value, normal_range, explanation, and suggestions.

        Report:
        {text}
        """

        response = model.generate_content(prompt)
        return {"analysis": response.text}

    except Exception as e:
        logger.exception("AI analysis failed")
        raise RuntimeError("Failed to analyze the medical report.") from e
