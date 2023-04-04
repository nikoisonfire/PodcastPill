from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api_service.models import Podcast, Category, Drops


# Util
def podcast_to_dict(row):
    to_dict = row.Podcast.__dict__
    # to_dict.pop("_sa_instance_state")

    drop_dict = row.Podcast.drops.__dict__
    drop_dict.pop("podcast_id")
    # drop_dict.pop("_sa_instance_state")

    categories = []
    for cat in row.Podcast.category:
        c_dict = cat.__dict__
        categories.append(c_dict["category"])
    # cat_dict.pop("_sa_instance_state")

    to_dict["drops"] = drop_dict
    to_dict["category"] = categories

    return to_dict


def get_all_podcasts(db: Session, limit: int = 100):
    pods = db.query(Podcast).limit(limit).all()
    return pods


def get_podcast(db: Session, podcast_id: int):
    statement = select(Podcast).where(Podcast.podcast_id == podcast_id)
    ex = db.execute(statement).first()
    return podcast_to_dict(ex)


def get_random_podcast(db: Session, weekday: str):
    row = db.query(Drops).filter(getattr(Drops, f"drops{weekday}") > 0).order_by(func.random()).first()
    return row.podcast.__dict__


def get_podcasts_by_category(db: Session, category: str, limit: int = 10):
    # cat = db.query(Podcast, Drops.dropsMonday).join(Category, Category.podcast_id == Podcast.podcast_id).filter(
    #   Category.category == category).filter(Drops.podcast_id == Podcast.podcast_id).limit(
    #  limit).all()
    statement = select(Podcast)
    ex = db.execute(statement).first()

    return podcast_to_dict(ex)


def get_categories(db: Session):
    query = db.query(Category.category).distinct().all()
    cats = [x for (x,) in query]
    return cats
