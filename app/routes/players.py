from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import PlayerResponse, PlayerUpdate
from app.services import player_service
from app.utils.image_handler import save_image

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("", response_model=list[PlayerResponse], summary="List players with filters and pagination")
def list_players(
    q: Optional[str] = Query(None, description="Search by name"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Results per page"),
    sort: str = Query("name", pattern="^(name|rating)$", description="Sort by name or rating"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort direction"),
    db: Session = Depends(get_db),
):
    return player_service.get_players(db, q=q, page=page, limit=limit, sort=sort, order=order)


@router.get("/{player_id}", response_model=PlayerResponse, summary="Get a player by ID")
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = player_service.get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail={"error": "Player not found"})
    return player


@router.post("", response_model=PlayerResponse, status_code=201, summary="Create a player (multipart/form-data)")
async def create_player(
    name: str = Form(..., description="Player name (required)"),
    country: Optional[str] = Form(None, description="Country"),
    club: Optional[str] = Form(None, description="Club"),
    image: Optional[UploadFile] = File(None, description="Profile image (JPG/PNG, max 1 MB)"),
    db: Session = Depends(get_db),
):
    image_url = None
    if image and image.filename:
        image_url = await save_image(image)

    data = {"name": name, "country": country, "club": club, "image_url": image_url}
    return player_service.create_player(db, data)


@router.put("/{player_id}", response_model=PlayerResponse, summary="Update a player")
def update_player(player_id: int, data: PlayerUpdate, db: Session = Depends(get_db)):
    player = player_service.update_player(db, player_id, data)
    if not player:
        raise HTTPException(status_code=404, detail={"error": "Player not found"})
    return player


@router.delete("/{player_id}", status_code=204, summary="Delete a player")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    deleted = player_service.delete_player(db, player_id)
    if not deleted:
        raise HTTPException(status_code=404, detail={"error": "Player not found"})
