from typing import Any, List, Optional

from pydantic import BaseModel, Field, field_validator


class PitchGenerationRequest(BaseModel):
    startup_idea: str = Field(..., min_length=10, max_length=1200)
    industry: str = Field(..., min_length=2, max_length=120)
    revenue_model: str = Field(..., min_length=3, max_length=240)

    @field_validator("startup_idea", "industry", "revenue_model")
    @classmethod
    def strip_text(cls, value: str) -> str:
        cleaned = " ".join(value.strip().split())
        if not cleaned:
            raise ValueError("Field cannot be blank")
        return cleaned


class PitchIdRequest(BaseModel):
    pitch_id: str = Field(..., min_length=8, max_length=64)


class ScoreRequest(PitchIdRequest):
    pass


class SWOTRequest(PitchIdRequest):
    pass


class CompetitorRequest(PitchIdRequest):
    pass


class ValuationRequest(PitchIdRequest):
    pass


class ExportRequest(PitchIdRequest):
    pass


def serialize_document(document: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
    if not document:
        return None

    serialized = {}
    for key, value in document.items():
        if key == "_id":
            serialized["id"] = str(value)
        elif hasattr(value, "isoformat"):
            serialized[key] = value.isoformat()
        elif isinstance(value, list):
            serialized[key] = [
                serialize_document(item) if isinstance(item, dict) else item for item in value
            ]
        elif isinstance(value, dict):
            serialized[key] = serialize_document(value)
        else:
            serialized[key] = value
    return serialized


PitchSectionList = List[str]
