from sqlalchemy import create_engine, Column, Integer, String
import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") else "sqlite:///nebby.db"
engine = create_engine(DATABASE_URL,echo=True)
Base = declarative_base()
