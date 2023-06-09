import logging

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api_service.models import Podcast, Category


# convert SQLalchemy model to python dict
def podcast_to_dict(row) -> dict:
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
def get_all_podcasts(db: Session, limit: int = 100) -> list:
    pods = db.query(Podcast).limit(limit).all()
    return pods


# get all categories
def get_all_categories(db: Session) -> dict:
    query = db.query(Category.category).distinct().all()
    # return count of items of each category
    query2 = db.query(Category.category, func.count(Category.category)).group_by(Category.category).all()
    logging.info(query2)
    cats = {x: y for (x, y) in query2 if y > 10}
    return cats


# get a podcast by id
def get_podcast(db: Session, podcast_id: int) -> dict:
    statement = select(Podcast).where(Podcast.podcast_id == podcast_id)
    ex = db.execute(statement).first()
    if ex is None:
        return None
    return podcast_to_dict(ex)


# get (limit) random podcasts, also use categories if provided
def get_random_podcast(db: Session, weekday: str, limit: int = 10, categories=None) -> list | dict:
    if categories is not None:
        logging.info("Categories are not none")
        statement = select(Podcast).join(Category, Category.podcast_id == Podcast.podcast_id).filter(
            Podcast.weekday == weekday).filter(Category.category.in_(categories)).order_by(
            func.random()).limit(limit)
        ex = db.execute(statement).all()
        if len(ex) == 0:
            return get_random_podcast(db, weekday, limit=1)
        return [podcast_to_dict(x) for x in ex]
    statement = select(Podcast).where(Podcast.weekday == weekday).order_by(func.random()).limit(limit)
    ex = db.execute(statement).all()

    return [podcast_to_dict(x) for x in ex]
    # return categories


# get an array of random podcasts, one for each day of the week
def get_random_week(db: Session, categories=None) -> list:
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


# get (limit) podcasts by category /podcasts/byCategory/{category}
def get_podcasts_by_category(db: Session, category: str, limit: int = 10) -> dict:
    statement = select(Category).where(Category.category == category).limit(limit)
    ex = db.execute(statement).all()
    if len(ex) == 0:
        return None
    # return [podcast_to_dict(x.Category.podcast) for x in ex]
    return [x.Category.podcast.__dict__ for x in ex]
