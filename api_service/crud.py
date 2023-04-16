import logging

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api_service.models import Podcast, Category


# convert SQLalchemy model to python dict
def podcast_to_dict(row):
    to_dict = row.Podcast.__dict__
    # to_dict.pop("_sa_instance_state")

    categories = []
    for cat in row.Podcast.category:
        c_dict = cat.__dict__
        categories.append(c_dict["category"])
    # cat_dict.pop("_sa_instance_state")

    to_dict["category"] = categories

    return to_dict


# get all podcasts --- this one might be unnecessary since there is no selector it will just load the first entries in db by default
def get_all_podcasts(db: Session, limit: int = 100):
    pods = db.query(Podcast).limit(limit).all()
    return pods


# get a podcast by id
def get_podcast(db: Session, podcast_id: int):
    statement = select(Podcast).where(Podcast.podcast_id == podcast_id)
    ex = db.execute(statement).first()
    return podcast_to_dict(ex)


# get (limit) random podcasts, also use categories if provided
def get_random_podcast(db: Session, weekday: str, limit: int = 10, categories=None):
    if categories is not None:
        logging.info("Categories are not none")
        statement = select(Podcast).join(Category, Category.podcast_id == Podcast.podcast_id).filter(
            Podcast.weekday == weekday).filter(Category.category.in_(categories)).order_by(
            func.random()).limit(limit)
        ex = db.execute(statement).all()
        return [podcast_to_dict(x) for x in ex]
    statement = select(Podcast).where(Podcast.weekday == weekday).order_by(func.random()).limit(limit)
    ex = db.execute(statement).all()

    return [podcast_to_dict(x) for x in ex]
    # return categories


# get an array of random podcasts, one for each day of the week
def get_random_week(db: Session, categories=None):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pod_list = []
    for day in weekdays:
        if categories is not None:
            res = get_random_podcast(db, day, limit=1, categories=categories)
            pod_list.append(res[0])
        else:
            res = get_random_podcast(db, day, limit=1)
            pod_list.append(res[0])
    return pod_list


# get (limit) podcasts by category
def get_podcasts_by_category(db: Session, category: str, limit: int = 10):
    statement = select(Category).where(Category.category == category).limit(limit)
    ex = db.execute(statement).all()

    # return [podcast_to_dict(x.Category.podcast) for x in ex]
    return [x.Category.podcast.__dict__ for x in ex]


# get (limit) random podcasts by category
def get_random_podcasts_by_category(db: Session, category: str, limit: int = 10):
    statement = select(Category).where(Category.category == category).limit(limit)
    ex = db.execute(statement).all()

    # return [podcast_to_dict(x.Category.podcast) for x in ex]
    return [x.Category.podcast.__dict__ for x in ex]


# get all categories
def get_categories(db: Session):
    query = db.query(Category.category).distinct().all()
    cats = [x for (x,) in query]
    return cats
