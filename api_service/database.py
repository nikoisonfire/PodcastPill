import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

package_dir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(package_dir, 'podpill.db')
# NEED 4 /'s to specify absolute for sqlalchemy!
# ex: sqlite:////asdfaijegoij/aerga.db
# NEED 3 /'s for relative paths
# path has a / at the beginning so we have 3 here
SQLALCHEMY_DATABASE_URL = ''.join(['sqlite:///', db_dir])

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True, echo_pool=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
