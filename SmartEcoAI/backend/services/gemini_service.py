import json
from dataclasses import asdict, dataclass

try:
    from google import genai
    from google.genai import types
except ImportError:  # pragma: no cover - handled gracefully at runtime
    genai = None
    types = None


@dataclass
class GeminiAnalysis:
    faces_detected: bool | None = None
    face_count: int | None = None
    scene_summary: str = ""
    policy_risk_level: str = "unknown"
    possible_concerns: list[str] = None
    recommended_action: str = ""
    confidence_note: str = ""
    raw_response: str = ""

    def __post_init__(self):
        if self.possible_concerns is None:
            self.possible_concerns = []


class GeminiService:
    def __init__(self, api_key: str, model: str = "gemini-3.6-flash"):
        self.api_key = api_key.strip()
        self.model = model

    def analyze_image(self, image_bytes: bytes, mime_type: str, filename: str = "") -> GeminiAnalysis:
        if genai is None or types is None:
            return GeminiAnalysis(
                scene_summary="The Gemini SDK is not installed.",
                policy_risk_level="unavailable",
                recommended_action="Install the google-genai package to enable image analysis.",
                confidence_note="The analysis service is unavailable until the dependency is installed.",
            )

        if not self.api_key:
            return GeminiAnalysis(
                scene_summary="Gemini API key is not configured.",
                policy_risk_level="unavailable",
                recommended_action="Set GEMINI_API_KEY in the environment to enable image analysis.",
                confidence_note="The analysis service is disabled until the API key is provided.",
            )

        try:
            client = genai.Client(api_key=self.api_key)
            prompt = (
                "You are reviewing a civic monitoring image for safety and operations.\n"
                "Identify whether any human faces are visibly present, estimate the face count if possible, "
                "and summarize the scene.\n"
                "Do NOT identify the person, infer identity, or claim something is illegal with certainty.\n"
                "Instead, provide a cautious policy-risk assessment based only on visible evidence.\n"
                f"Image filename: {filename or 'upload'}.\n"
                "Return only valid JSON with these keys:\n"
                "{"
                '"faces_detected": boolean, '
                '"face_count": integer or null, '
                '"scene_summary": string, '
                '"policy_risk_level": "low" | "medium" | "high" | "unknown", '
                '"possible_concerns": array of strings, '
                '"recommended_action": string, '
                '"confidence_note": string'
                "}."
            )

            response = client.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    prompt,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )

            raw_text = (response.text or "").strip()
            parsed = self._parse_json(raw_text)
            analysis = GeminiAnalysis(raw_response=raw_text)

            if parsed:
                analysis.faces_detected = parsed.get("faces_detected")
                analysis.face_count = parsed.get("face_count")
                analysis.scene_summary = parsed.get("scene_summary", "")
                analysis.policy_risk_level = parsed.get("policy_risk_level", "unknown")
                analysis.possible_concerns = parsed.get("possible_concerns", []) or []
                analysis.recommended_action = parsed.get("recommended_action", "")
                analysis.confidence_note = parsed.get("confidence_note", "")
            else:
                analysis.scene_summary = raw_text or "No structured response was returned."
                analysis.policy_risk_level = "unknown"
                analysis.recommended_action = "Review the image manually."
                analysis.confidence_note = "Gemini returned a non-JSON response."

            return analysis
        except Exception as exc:  # pragma: no cover - runtime safety
            return GeminiAnalysis(
                scene_summary="Gemini analysis failed.",
                policy_risk_level="unavailable",
                recommended_action="Check your API key, network access, and model name.",
                confidence_note=str(exc),
            )

    def _parse_json(self, raw_text: str) -> dict | None:
        if not raw_text:
            return None

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            start = raw_text.find("{")
            end = raw_text.rfind("}")
            if start == -1 or end == -1 or end <= start:
                return None
            try:
                return json.loads(raw_text[start : end + 1])
            except json.JSONDecodeError:
                return None


def analysis_to_dict(analysis: GeminiAnalysis) -> dict:
    return asdict(analysis)
