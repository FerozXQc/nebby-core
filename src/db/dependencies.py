from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") else "sqlite:///nebby.db"
engine = create_engine(DATABASE_URL,echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#db session
def get_db():
    try:
        db = SessionLocal()
        yield db
    except:
        db.rollback()
    finally:
        db.close()
