from fastapi import FastAPI

from api_service import models
from api_service.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/podcasts/{podcast_id}")
async def get_podcast(podcast_id: int):
    return {"podcast_id": podcast_id}


@app.get("/podcasts/random/{weekday}")
async def get_random_podcast(weekday: str):
    return {"weekday": weekday}


@app.get("/podcasts/byCategory/{category}")
async def get_podcast_by_category(category: str):
    return {"category": category}


@app.get("/categories")
async def get_categories():
    return {"categories": ["category1", "category2", "category3"]}
