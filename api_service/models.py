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
    weekday: str = Column(String, index=True)

    category: Mapped[List["Category"]] = relationship("Category", back_populates="podcast")


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
