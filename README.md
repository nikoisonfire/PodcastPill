# PodcastPill

PodcastPill let's you generate a weekly schedule to listen to a new podcast every single day.

[Demo](https://podcastpill.netlify.app/)

[Frontend](https://github.com/nikoisonfire/pp_frontend)

# Folders

- api_service: FastAPI backend / SQLA models and operations
- db_service: SQLite database controller
- pull_service: PodcastIndex.org API wrapper, pulls podcast data and episodes
- scripting: random jupyter notebooks for testing

# Install and use

1. Clone the repo
2. Start the venv with `source venv/bin/activate`
3. Install dependencies with `pip install -r requirements.txt`
4. Run the backend with `uvicorn api_service.main:app --reload`
5. Start coding