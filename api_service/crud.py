from sqlalchemy import func
from sqlalchemy.orm import Session

from api_service.models import Podcast, Category, Drops


def get_podcast(db: Session, podcast_id: int):
    return db.query(Podcast).filter(Podcast.id == podcast_id).first()


def get_random_podcast(db: Session, weekday: str):
    drops = db.query(Drops).filter(getattr(Drops, f"drops{weekday}") == 1).orderBy(func.random()).first()
    return db.query(Podcast).filter(drops.podcast_id).first()


def get_podcasts_by_category(db: Session, category: str, limit: int = 10):
    cat = db.query(Category).filter(Category.category == category).limit(limit).all()
    return cat


def get_categories(db: Session):
    # return db.query(Category.category).distinct().all()
    # logging.info(db.connection())
    return {}
