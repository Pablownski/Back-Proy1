from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import RankingCreate, RankingUpdate, RankingResponse, TierResponse
from app.services import ranking_service

router = APIRouter(prefix="/ranking", tags=["Ranking"])


@router.get("", response_model=list[TierResponse], summary="Get full tier list grouped by tier")
def get_ranking(db: Session = Depends(get_db)):
    return ranking_service.get_ranking(db)


@router.post("", response_model=RankingResponse, status_code=201, summary="Add a player to the ranking")
def create_ranking(data: RankingCreate, db: Session = Depends(get_db)):
    if not ranking_service.player_exists(db, data.player_id):
        raise HTTPException(status_code=404, detail={"error": "Player not found"})

    result = ranking_service.create_ranking(db, data)
    if result is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "Player is already in the ranking"},
        )
    return result


@router.put("/{ranking_id}", response_model=RankingResponse, summary="Update a ranking entry")
def update_ranking(ranking_id: int, data: RankingUpdate, db: Session = Depends(get_db)):
    result = ranking_service.update_ranking(db, ranking_id, data)
    if result is None:
        raise HTTPException(status_code=404, detail={"error": "Ranking entry not found"})
    return result


@router.delete("/{ranking_id}", status_code=204, summary="Remove a player from the ranking")
def delete_ranking(ranking_id: int, db: Session = Depends(get_db)):
    deleted = ranking_service.delete_ranking(db, ranking_id)
    if not deleted:
        raise HTTPException(status_code=404, detail={"error": "Ranking entry not found"})
