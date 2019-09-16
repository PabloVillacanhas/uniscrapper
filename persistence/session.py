from sqlalchemy.orm import sessionmaker
from persistence import engine

sessionconf = sessionmaker(bind=engine)
session = sessionconf()
