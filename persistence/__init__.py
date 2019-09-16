__name__ = "persistence"

import sqlalchemy as db
from . import models
from sqlalchemy_utils import database_exists, create_database

stringconn = "mysql+pymysql://dbadmin:dbadmin@localhost:3306/uniscrapper"
engine = db.create_engine(stringconn, isolation_level="REPEATABLE_READ", echo=True)
if not database_exists(engine.url):
    opt = input("No database encountered, create new one? Y/n ")
    if opt == 'y' or opt == 'Y':
        create_database(engine.url)
        r = models.Base.metadata.create_all(engine)
        print("Database created ", r)
