import logging
from typing import Annotated

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from api_service import crud, models
from api_service.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.info(e)
    finally:
        db.close()


# return nothing on default
@app.get("/")
def root():
    return {}


@app.get("/podcasts/{podcast_id}")
def get_podcast(podcast_id: int, db: Session = Depends(get_db)):
    return crud.get_podcast(db, podcast_id=podcast_id)


@app.get("/podcasts")
def get_podcast(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_podcasts(db, limit=limit)


@app.get("/random/{weekday}")
def get_random_podcast(weekday: str, db: Session = Depends(get_db), limit: int = 10,
                       cat: Annotated[list[str] | None, Query()] = None):
    return crud.get_random_podcast(db, weekday=weekday, categories=cat, limit=limit)


@app.get("/random-week")
def get_random_week(db: Session = Depends(get_db), cat: Annotated[list[str] | None, Query()] = None):
    return crud.get_random_week(db, categories=cat)


@app.get("/podcasts/byCategory/{category}")
def get_podcast_by_category(category: str, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_podcasts_by_category(db, limit=limit, category=category)


@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return {
        "categories": crud.get_categories(db)
    }
