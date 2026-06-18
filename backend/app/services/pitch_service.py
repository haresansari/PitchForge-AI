from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from bson import ObjectId

from app.database.connection import get_db
from app.models.pitch import serialize_document

memory_store: dict[str, dict[str, Any]] = {}


class PitchService:
    @staticmethod
    def create_pitch(pitch_data: dict[str, Any]) -> str:
        now = datetime.utcnow()
        document = {
            **pitch_data,
            "scores": None,
            "swot": None,
            "competitors": None,
            "valuation": None,
            "created_at": now,
            "updated_at": now,
        }

        db = get_db()
        if db is None:
            pitch_id = uuid4().hex
            document["_id"] = pitch_id
            memory_store[pitch_id] = document
            return pitch_id

        result = db.pitches.insert_one(document)
        return str(result.inserted_id)

    @staticmethod
    def get_pitch(pitch_id: str) -> Optional[dict[str, Any]]:
        db = get_db()
        if db is None:
            return serialize_document(memory_store.get(pitch_id))

        try:
            return serialize_document(db.pitches.find_one({"_id": ObjectId(pitch_id)}))
        except Exception:
            return None

    @staticmethod
    def update_section(pitch_id: str, section: str, data: dict[str, Any]) -> bool:
        data["timestamp"] = datetime.utcnow()
        now = datetime.utcnow()
        db = get_db()

        if db is None:
            if pitch_id not in memory_store:
                return False
            memory_store[pitch_id][section] = data
            memory_store[pitch_id]["updated_at"] = now
            return True

        try:
            result = db.pitches.update_one(
                {"_id": ObjectId(pitch_id)},
                {"$set": {section: data, "updated_at": now}},
            )
            return result.matched_count == 1
        except Exception:
            return False

    @staticmethod
    def get_history(limit: int = 10, skip: int = 0) -> list[dict[str, Any]]:
        db = get_db()
        if db is None:
            rows = sorted(memory_store.values(), key=lambda item: item["created_at"], reverse=True)
            return [serialize_document(row) for row in rows[skip : skip + limit]]

        cursor = (
            db.pitches.find(
                {},
                {
                    "startup_name": 1,
                    "industry": 1,
                    "elevator_pitch": 1,
                    "created_at": 1,
                    "scores": 1,
                },
            )
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )
        return [serialize_document(row) for row in cursor]
