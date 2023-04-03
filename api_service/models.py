from dataclasses import dataclass
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped

from api_service.database import Base


@dataclass
class Podcast(Base):
    __tablename__ = "podcasts"

    podcast_id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, index=True)
    description: str = Column(String, index=True)
    image: str = Column(String, index=True)

    category: Mapped[List["Category"]] = relationship("Category", back_populates="podcast")
    drops: Mapped["Drops"] = relationship("Drops", back_populates="podcast")


@dataclass
class Category(Base):
    __tablename__ = "categories"

    cat_id: int
    podcast_id: int
    category: str

    cat_id: int = Column(Integer, primary_key=True, index=True)
    podcast_id: int = Column(Integer, ForeignKey("podcasts.podcast_id"))
    category: str = Column(String, index=True)
    podcast: Mapped["Podcast"] = relationship("Podcast", back_populates="category")


@dataclass
class Drops(Base):
    __tablename__ = "drops"
    
    podcast_id: int = Column(Integer, ForeignKey("podcasts.podcast_id"), primary_key=True, index=True)
    dropsMonday: float = Column(Integer, index=True)
    dropsTuesday: float = Column(Integer, index=True)
    dropsWednesday: float = Column(Integer, index=True)
    dropsThursday: float = Column(Integer, index=True)
    dropsFriday: float = Column(Integer, index=True)
    dropsSaturday: float = Column(Integer, index=True)
    dropsSunday: float = Column(Integer, index=True)
    podcast: Mapped["Podcast"] = relationship("Podcast", back_populates="drops")
