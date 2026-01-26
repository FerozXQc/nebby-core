from pydantic import BaseModel

class registerUserSchema(BaseModel):
    name: str
    email: str
    password: str

class loginUserSchema(BaseModel):
    email: str
    password: str