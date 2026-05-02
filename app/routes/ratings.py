from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import RatingCreate, RatingsListResponse
from app.services import rating_service

router = APIRouter(prefix="/players", tags=["Ratings"])


@router.post(
    "/{player_id}/ratings",
    status_code=201,
    summary="Add a rating to a player",
)
def add_rating(player_id: int, data: RatingCreate, db: Session = Depends(get_db)):
    if not rating_service.player_exists(db, player_id):
        raise HTTPException(status_code=404, detail={"error": "Player not found"})
    return rating_service.add_rating(db, player_id, data)


@router.get(
    "/{player_id}/ratings",
    response_model=RatingsListResponse,
    summary="Get all ratings for a player",
)
def get_ratings(player_id: int, db: Session = Depends(get_db)):
    if not rating_service.player_exists(db, player_id):
        raise HTTPException(status_code=404, detail={"error": "Player not found"})
    return rating_service.get_ratings(db, player_id)
