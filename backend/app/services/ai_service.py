import hashlib
import json
import os
import random
import re
from typing import Any

import google.generativeai as genai
import os


from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None


class AIService:
    @staticmethod
    def _model():
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or genai is None:
            return None
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))

    @staticmethod
    def _json_from_model(prompt: str) -> dict[str, Any]:
        model = AIService._model()
        if model is None:
            raise RuntimeError("Gemini API key is not configured")

        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.72, "response_mime_type": "application/json"},
        )
        text = response.text.strip()
        text = re.sub(r"^```json|```$", "", text).strip()
        return json.loads(text)

    @staticmethod
    def generate_pitch(startup_idea: str, industry: str, revenue_model: str) -> dict[str, Any]:
        prompt = f"""
You are a venture studio partner. Generate a concise investor-ready startup pitch.
Return valid JSON only with these keys:
startup_name, elevator_pitch, problem_statement, solution, business_model,
revenue_streams array, market_opportunity, investor_summary.

Startup idea: {startup_idea}
Industry: {industry}
Revenue model: {revenue_model}
Tone: premium, specific, credible, founder-friendly, not hype-heavy.
"""
        try:
            return AIService._json_from_model(prompt)
        except Exception:
            return AIService._fallback_pitch(startup_idea, industry, revenue_model)

    @staticmethod
    def generate_scores(pitch_data: dict[str, Any]) -> dict[str, Any]:
        prompt = f"""
Score this startup pitch from 0 to 100. Return JSON only:
innovation_score, market_demand_score, scalability_score, investor_appeal_score.
Pitch: {json.dumps(pitch_data, default=str)}
"""
        try:
            result = AIService._json_from_model(prompt)
        except Exception:
            result = AIService._fallback_scores(pitch_data)

        for key in [
            "innovation_score",
            "market_demand_score",
            "scalability_score",
            "investor_appeal_score",
        ]:
            result[key] = max(0, min(100, int(result.get(key, 72))))
        result["overall_score"] = sum(result[key] for key in result if key.endswith("_score")) // 4
        return result

    @staticmethod
    def generate_swot(pitch_data: dict[str, Any]) -> dict[str, Any]:
        prompt = f"""
Create a practical SWOT analysis for this startup. Return JSON only with arrays:
strengths, weaknesses, opportunities, threats.
Pitch: {json.dumps(pitch_data, default=str)}
"""
        try:
            return AIService._json_from_model(prompt)
        except Exception:
            return {
                "strengths": [
                    "Clear customer pain with measurable business value.",
                    "Focused positioning makes the first buyer segment easy to target.",
                    "Software-led delivery can improve margins as usage grows.",
                ],
                "weaknesses": [
                    "Early credibility depends on strong customer proof points.",
                    "The product needs disciplined scope control before scaling.",
                ],
                "opportunities": [
                    "Partner with accelerators, campus programs, and founder communities.",
                    "Package benchmark data into premium insights for teams and investors.",
                ],
                "threats": [
                    "Incumbents could add similar workflows to broader platforms.",
                    "Customer acquisition costs may rise in crowded startup channels.",
                ],
            }

    @staticmethod
    def generate_competitors(pitch_data: dict[str, Any]) -> dict[str, Any]:
        prompt = f"""
Generate a competitor analysis. Return JSON only:
competitors array of objects with name, strengths array, weaknesses, market_position,
and market_insights string.
Pitch: {json.dumps(pitch_data, default=str)}
"""
        try:
            return AIService._json_from_model(prompt)
        except Exception:
            industry = pitch_data.get("industry", "startup software")
            return {
                "competitors": [
                    {
                        "name": f"Legacy {industry.title()} Platforms",
                        "strengths": ["Existing distribution", "Known brand trust"],
                        "weaknesses": "Often expensive, slow to configure, and built for larger teams.",
                        "market_position": "Established incumbents",
                    },
                    {
                        "name": "Horizontal AI Workspaces",
                        "strengths": ["Flexible workflows", "Broad AI utility"],
                        "weaknesses": "Generic outputs and limited vertical investor context.",
                        "market_position": "Fast-moving substitutes",
                    },
                    {
                        "name": "Boutique Consulting Services",
                        "strengths": ["High-touch guidance", "Custom strategic advice"],
                        "weaknesses": "Difficult to scale and costly for early founders.",
                        "market_position": "Premium services alternative",
                    },
                ],
                "market_insights": "The strongest wedge is a focused product that combines speed, structure, and credible investor framing for underserved early-stage teams.",
            }

    @staticmethod
    def generate_valuation(pitch_data: dict[str, Any]) -> dict[str, Any]:
        prompt = f"""
Estimate an early-stage startup valuation range. Return JSON only:
low_estimate, medium_estimate, high_estimate, reasoning.
Pitch: {json.dumps(pitch_data, default=str)}
"""
        try:
            return AIService._json_from_model(prompt)
        except Exception:
            seed = AIService._seed(pitch_data.get("startup_name", "startup"))
            low = 1 + seed % 3
            mid = low + 2 + seed % 4
            high = mid + 4 + seed % 6
            return {
                "low_estimate": f"${low}M - ${low + 2}M",
                "medium_estimate": f"${mid}M - ${mid + 4}M",
                "high_estimate": f"${high}M - ${high + 8}M",
                "reasoning": "Indicative range based on pre-seed to seed-stage software comparables, market clarity, scalability, and investor narrative strength.",
            }

    @staticmethod
    def _seed(value: str) -> int:
        return int(hashlib.sha256(value.encode("utf-8")).hexdigest()[:8], 16)

    @staticmethod
    def _fallback_pitch(startup_idea: str, industry: str, revenue_model: str) -> dict[str, Any]:
        keywords = re.findall(r"[A-Za-z]{4,}", startup_idea)
        root = keywords[0].title() if keywords else industry.title()
        suffix = random.Random(AIService._seed(startup_idea)).choice(["Forge", "Pilot", "Layer", "Nexus"])
        name = f"{root}{suffix}"

        return {
            "startup_name": name,
            "elevator_pitch": f"{name} helps {industry.lower()} teams turn fragmented workflows into a faster, data-backed operating system with a {revenue_model.lower()} model.",
            "problem_statement": f"Customers in {industry.lower()} still rely on disconnected tools, manual decision-making, and inconsistent execution. This creates avoidable delays, weak visibility, and higher operating costs just as teams need to move faster.",
            "solution": f"{name} gives users a guided platform that captures intent, structures the workflow, and produces actionable recommendations in minutes. The product reduces manual effort while creating a repeatable system for better decisions.",
            "business_model": f"The company will monetize through {revenue_model.lower()}, with expansion potential through team seats, premium analytics, implementation support, and partner channels.",
            "revenue_streams": [
                "Subscription tiers for individuals and teams",
                "Premium analytics and workflow automation add-ons",
                "Enterprise onboarding and partner program fees",
            ],
            "market_opportunity": f"The {industry.lower()} market is large, fragmented, and actively adopting AI-enabled productivity software. A focused vertical product can win early adopters by delivering faster outcomes than generic tools.",
            "investor_summary": f"{name} has a clear wedge, recurring revenue potential, and a credible path from niche adoption to platform expansion. The opportunity is compelling if the team can prove retention, distribution efficiency, and repeatable customer value.",
        }

    @staticmethod
    def _fallback_scores(pitch_data: dict[str, Any]) -> dict[str, Any]:
        seed = AIService._seed(json.dumps(pitch_data, default=str))
        return {
            "innovation_score": 74 + seed % 17,
            "market_demand_score": 72 + (seed // 3) % 18,
            "scalability_score": 70 + (seed // 5) % 20,
            "investor_appeal_score": 71 + (seed // 7) % 18,
        }


# def generate_pitch(idea: str):
#    pass