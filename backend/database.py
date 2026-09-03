import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Fetch the URL we just added to the .env file
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory to handle database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The base class that all our models will inherit from
Base = declarative_base()