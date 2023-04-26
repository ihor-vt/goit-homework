# import configparser
# import pathlib

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.conf.config import settings

# Docker: docker run --name db-postgres -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres
# URI:  postgresql://username:password@domain:port/database
# file_config = pathlib.Path(__file__).parent.parent.joinpath("conf/config.ini")
# config = configparser.ConfigParser()
# config.read(file_config)

# username = config.get("DEV_DB", "USER")
# password = config.get("DEV_DB", "PASSWORD")
# domain = config.get("DEV_DB", "DOMAIN")
# port = config.get("DEV_DB", "PORT")
# database = config.get("DEV_DB", "DB_NAME")

# URI = f"postgresql://{username}:{password}@{domain}:{port}/{database}"

URI = settings.sqlalchemy_database_url

engine = create_engine(URI, echo=True)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
