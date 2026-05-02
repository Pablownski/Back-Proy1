from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=True)
    club = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    ratings = relationship("Rating", back_populates="player", cascade="all, delete-orphan")
    ranking = relationship("Ranking", back_populates="player", uselist=False, cascade="all, delete-orphan")


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False)

    player = relationship("Player", back_populates="ratings")


class Ranking(Base):
    __tablename__ = "ranking"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, unique=True)
    tier = Column(String, nullable=False)
    position = Column(Integer, nullable=False)

    player = relationship("Player", back_populates="ranking")
