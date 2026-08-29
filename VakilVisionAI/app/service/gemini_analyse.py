import json

from google import genai
from google.genai import types

from config import GEMINI_API_KEY
from service.prompt import CONTRACT_ANALYSIS_PROMPT
from models import CaluseAnalysis, AnalysisResult, RiskFlag

GEMINI_MODEL = "gemini-3.5-flash"

client = genai.Client(api_key=GEMINI_API_KEY)


def _extract_json(raw: str) -> dict:
    """Parse the model output, tolerating ```json fences around the object."""
    text = (raw or "").strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.lstrip().lower().startswith("json"):
            text = text.lstrip()[4:]
    return json.loads(text.strip())


async def analyse_contract(contract_id: str, text_content: str):
    prompt = CONTRACT_ANALYSIS_PROMPT.format(contract_text=text_content[:15000])

    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        ),
    )

    analyse_data = _extract_json(response.text)

    key_clauses = [
        CaluseAnalysis(**clause)
        for clause in analyse_data.get("key_clauses", [])
    ]
    risk_flags = [
        RiskFlag(**risk)
        for risk in analyse_data.get("risk_flags", [])
    ]

    return AnalysisResult(
        contract_id=contract_id,
        summary=analyse_data.get("summary", ""),
        contract_type=analyse_data.get("contract_type", "Unknown"),
        key_clauses=key_clauses,
        risk_flags=risk_flags,
        overall_risk_level=analyse_data.get("overall_risk_level", "low"),
        recommendation=analyse_data.get("recommendations", []),
    )
