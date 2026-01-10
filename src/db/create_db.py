from src.db.dependencies import Base, engine
from src.db.models import *
Base.metadata.create_all(bind=engine)