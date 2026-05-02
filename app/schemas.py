from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


# ── Players ────────────────────────────────────────────────────────────────────

class PlayerCreate(BaseModel):
    name: str
    country: Optional[str] = None
    club: Optional[str] = None


class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    club: Optional[str] = None
    image_url: Optional[str] = None


class PlayerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    country: Optional[str] = None
    club: Optional[str] = None
    image_url: Optional[str] = None
    avg_rating: Optional[float] = None


# ── Ratings ────────────────────────────────────────────────────────────────────

class RatingCreate(BaseModel):
    score: float = Field(..., ge=1, le=10, description="Score between 1 and 10")


class RatingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    player_id: int
    score: float


class RatingsListResponse(BaseModel):
    ratings: List[RatingResponse]
    avg_rating: Optional[float] = None


# ── Ranking ────────────────────────────────────────────────────────────────────

class RankingCreate(BaseModel):
    player_id: int
    tier: str = Field(..., description="Tier label: S, A, B, C, D, F")
    position: int = Field(..., ge=1)


class RankingUpdate(BaseModel):
    tier: Optional[str] = None
    position: Optional[int] = Field(None, ge=1)


class RankingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    player_id: int
    tier: str
    position: int


class TierPlayerResponse(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    rating: Optional[float] = None


class TierResponse(BaseModel):
    tier: str
    players: List[TierPlayerResponse]
