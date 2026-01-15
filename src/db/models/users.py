from src.db.dependencies import Base
from src.utils.generate_uuid import generate_uuid
from sqlalchemy import String, Integer, Column
from sqlalchemy.dialects.postgresql import UUID
class UserModel(Base):
    __tablename__ = "nebby-users"
    id = Column(UUID(as_uuid=True), primary_key=True,default=generate_uuid)
    name = Column(String(50), nullable=False)
    email = Column(String, nullable=False,unique=True)
    hashed_password = Column(String, nullable=False)