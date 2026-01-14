from src.db.models.users import UserModel as model
from sqlalchemy.orm import Session
from src.db.schemas.auth_schema import registerUserSchema
from src.utils.password import generate_hashed_password
class AuthRepository():
    def __init__(self,Session):
        self.session = Session
        self.model = model
    
    def fetch_user_by_id(self,id:uuid):
        return self.session.query(self.model).filter(self.model.id == id).first()
    
    def fetch_user_by_email(self,email:str):
        return self.session.query(self.model).filter(self.model.email == email).first()

    def create_user(self,register_schema:registerUserSchema):
        try:
            user_payload = {
                "name": register_schema.name,
                "email": register_schema.email,
                "hashed_password": generate_hashed_password(register_schema.password)
            }
            user_record = self.model(**user_payload)
            self.session.add(user_record)
            self.session.commit()
            self.session.refresh(user_record)
            return user_record
        except Exception as e:
            self.session.rollback()
            raise