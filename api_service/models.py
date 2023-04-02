from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api_service.database import Base


@dataclass
class Podcast(Base):
    __tablename__ = "podcasts"

    id: int
    title: str
    description: str
    image: str

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    image = Column(String, index=True)

    category = relationship("Category", back_populates="podcast")
    drops = relationship("Drops", back_populates="podcast")


@dataclass
class Category(Base):
    __tablename__ = "categories"

    id: int
    podcast_id: int
    category: str

    id = Column(Integer, primary_key=True, index=True)
    podcast_id = Column(Integer, ForeignKey("podcasts.id"))
    category = Column(String, index=True)
    podcast = relationship("Podcast", back_populates="category")


@dataclass
class Drops(Base):
    __tablename__ = "drops"

    id: int
    podcast_id: int
    dropsMonday: int
    dropsTuesday: int
    dropsWednesday: int
    dropsThursday: int
    dropsFriday: int
    dropsSaturday: int
    dropsSunday: int

    id = Column(Integer, primary_key=True, index=True)
    podcast_id = Column(Integer, ForeignKey("podcasts.id"))
    dropsMonday = Column(Integer, index=True)
    dropsTuesday = Column(Integer, index=True)
    dropsWednesday = Column(Integer, index=True)
    dropsThursday = Column(Integer, index=True)
    dropsFriday = Column(Integer, index=True)
    dropsSaturday = Column(Integer, index=True)
    dropsSunday = Column(Integer, index=True)
    podcast = relationship("Podcast", back_populates="drops")
