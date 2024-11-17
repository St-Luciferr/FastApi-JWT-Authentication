from sqlalchemy import create_engine
# from models.database import Base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os

from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy Database setup
engine = create_engine(DATABASE_URL) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Pass the session to the route
    finally:
        db.close()  # Ensure the session is closed when done