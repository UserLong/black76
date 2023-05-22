import sqlalchemy as db
from sqlalchemy.orm import declarative_base, sessionmaker

APP_DATABASE_URL = "sqlite:///options_data.db"

engine = db.create_engine(APP_DATABASE_URL, echo=True)

Base = declarative_base()

Session  = sessionmaker(autocommit=False, autoflush=False, bind=engine)