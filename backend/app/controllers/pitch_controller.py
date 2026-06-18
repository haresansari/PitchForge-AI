from app.services.ai_service import AIService
from app.services.pitch_service import PitchService


class PitchController:
    @staticmethod
    def generate_pitch(startup_idea: str, industry: str, revenue_model: str) -> dict:
        pitch_data = AIService.generate_pitch(startup_idea, industry, revenue_model)
        pitch_data.update(
            {
                "original_idea": startup_idea,
                "industry": industry,
                "revenue_model": revenue_model,
            }
        )
        pitch_id = PitchService.create_pitch(pitch_data)
        saved_pitch = PitchService.get_pitch(pitch_id)
        return {"success": True, "pitch_id": pitch_id, "data": saved_pitch}

    @staticmethod
    def generate_scores(pitch_id: str) -> dict:
        pitch = PitchService.get_pitch(pitch_id)
        if not pitch:
            return {"success": False, "error": "Pitch not found"}
        scores = AIService.generate_scores(pitch)
        PitchService.update_section(pitch_id, "scores", scores)
        return {"success": True, "data": PitchService.get_pitch(pitch_id)}

    @staticmethod
    def generate_swot(pitch_id: str) -> dict:
        pitch = PitchService.get_pitch(pitch_id)
        if not pitch:
            return {"success": False, "error": "Pitch not found"}
        swot = AIService.generate_swot(pitch)
        PitchService.update_section(pitch_id, "swot", swot)
        return {"success": True, "data": PitchService.get_pitch(pitch_id)}

    @staticmethod
    def generate_competitors(pitch_id: str) -> dict:
        pitch = PitchService.get_pitch(pitch_id)
        if not pitch:
            return {"success": False, "error": "Pitch not found"}
        competitors = AIService.generate_competitors(pitch)
        PitchService.update_section(pitch_id, "competitors", competitors)
        return {"success": True, "data": PitchService.get_pitch(pitch_id)}

    @staticmethod
    def generate_valuation(pitch_id: str) -> dict:
        pitch = PitchService.get_pitch(pitch_id)
        if not pitch:
            return {"success": False, "error": "Pitch not found"}
        valuation = AIService.generate_valuation(pitch)
        PitchService.update_section(pitch_id, "valuation", valuation)
        return {"success": True, "data": PitchService.get_pitch(pitch_id)}

    @staticmethod
    def get_pitch_detail(pitch_id: str) -> dict:
        pitch = PitchService.get_pitch(pitch_id)
        if not pitch:
            return {"success": False, "error": "Pitch not found"}
        return {"success": True, "data": pitch}

    @staticmethod
    def get_history(limit: int = 10, skip: int = 0) -> dict:
        return {"success": True, "data": PitchService.get_history(limit, skip)}
