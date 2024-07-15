import sqlite3
from sqlalchemy import create_engine,select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///Recetario/Recetario/res/database.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
