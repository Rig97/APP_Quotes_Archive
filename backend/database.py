# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()  # Reads the .env file from the project root


# Build the database URL from .env values
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME')


DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# Create the engine (the connection pool to the database)
engine = create_engine(DATABASE_URL)


# SessionLocal is a factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for all our database models
Base = declarative_base()


# Dependency: used in every route to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
