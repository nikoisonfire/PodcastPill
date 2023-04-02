import logging

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from api_service import models, crud
from api_service.database import engine, SessionLocal

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/podcasts/{podcast_id}")
async def get_podcast(podcast_id: int, db: Session = Depends(get_db)):
    return crud.get_podcast(db, podcast_id=podcast_id)


@app.get("/podcasts/random/{weekday}")
async def get_random_podcast(weekday: str, db: Session = Depends(get_db)):
    return crud.get_random_podcast(db, weekday=weekday)


@app.get("/podcasts/byCategory/{category}")
async def get_podcast_by_category(category: str, db: Session = Depends(get_db)):
    return crud.get_podcasts_by_category(db, category=category)


@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return {
        "queries": crud.get_categories(db)
    }
