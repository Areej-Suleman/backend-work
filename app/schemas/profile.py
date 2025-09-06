from pydantic import BaseModel, field_validator
from typing import Optional, List, Any
import json


def _to_list(value: Any) -> Optional[List[str]]:
    if value is None:
        return None
    if isinstance(value, list):
        return [str(v) for v in value]
    # Try JSON first
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(v) for v in parsed]
    except Exception:
        pass
    # Fallback: parse comma-separated or bracketed strings
    s = str(value).strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    parts = [p.strip().strip("'\"") for p in s.split(',') if p.strip()]
    return parts if parts else None


class ProfileBase(BaseModel):
    skin_type: Optional[str] = None
    skin_tone: Optional[str] = None
    skin_concerns: Optional[List[str]] = None
    allergies: Optional[List[str]] = None

    @field_validator("skin_concerns", "allergies", mode="before")
    @classmethod
    def _parse_lists(cls, v):
        return _to_list(v)


class ProfileCreate(ProfileBase):
    user_id: int

class ProfileUpdate(ProfileBase):
    pass

class ProfilePreferences(BaseModel):
    preferred_brands: Optional[List[str]] = None
    budget_range: Optional[str] = None

    @field_validator("preferred_brands", mode="before")
    @classmethod
    def _parse_pref_brands(cls, v):
        return _to_list(v)


class Profile(BaseModel):
    id: int
    user_id: int
    skin_type: Optional[str] = None
    skin_tone: Optional[str] = None
    skin_concerns: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    preferred_brands: Optional[List[str]] = None
    budget_range: Optional[str] = None
    skin_sensitivity: Optional[str] = None
    current_routine: Optional[str] = None
    goals: Optional[str] = None

    @field_validator("skin_concerns", "allergies", "preferred_brands", mode="before")
    @classmethod
    def _parse_out_lists(cls, v):
        return _to_list(v)

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2
