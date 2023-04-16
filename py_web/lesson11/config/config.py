import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'data' / 'lesson11.db.sqlite3')
    SECRET_KEY = '%$#%^&%%^&&(&'