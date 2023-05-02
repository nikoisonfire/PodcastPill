import logging
from typing import Annotated

from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from api_service import crud, models
from api_service.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Test workflow123


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
    raise HTTPException(status_code=404, detail="Page not found")


@app.get("/podcasts/{podcast_id}")
def get_podcast(podcast_id: int, db: Session = Depends(get_db)):
    podcast = crud.get_podcast(db, podcast_id=podcast_id)
    if podcast is None:
        raise HTTPException(status_code=404, detail="Podcast not found")
    return podcast


@app.get("/podcasts")
def get_podcast(limit: int = 10, db: Session = Depends(get_db)):
    podcasts = crud.get_all_podcasts(db, limit=limit)
    if podcasts is None:
        raise HTTPException(status_code=404, detail="No podcasts found")
    return podcasts


@app.get("/random/{weekday}")
def get_random_podcast(weekday: str, db: Session = Depends(get_db), limit: int = 10,
                       cat: Annotated[list[str] | None, Query()] = None):
    podcast = crud.get_random_podcast(db, weekday=weekday, categories=cat, limit=limit)
    if podcast is None:
        raise HTTPException(status_code=404, detail="No podcast found")
    return podcast


@app.get("/random-week")
def get_random_week(db: Session = Depends(get_db), cat: Annotated[list[str] | None, Query()] = None):
    response = crud.get_random_week(db, categories=cat)
    if response is None:
        raise HTTPException(status_code=404, detail="No podcasts found")
    return response


@app.get("/podcasts/byCategory/{category}")
def get_podcast_by_category(category: str, limit: int = 10, db: Session = Depends(get_db)):
    podcasts = crud.get_podcasts_by_category(db, limit=limit, category=category)
    if podcasts is None:
        raise HTTPException(status_code=404, detail="No podcasts found")
    return podcasts


@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = crud.get_all_categories(db)
    if categories is None:
        raise HTTPException(status_code=404, detail="No categories found")
    return {
        "categories": categories
    }
