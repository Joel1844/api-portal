from fastapi import APIRouter, BackgroundTasks
from pydantic import Field, BaseModel, EmailStr
from pymongo.collection import Collection


from config.db import DbRed

from typing import Optional
# from utils import hash_password, verify_password
from bson.objectid import ObjectId


class Base_User(BaseModel):
    __collection__: str = "users"

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }

class Login(Base_User,BaseModel):
    correo:EmailStr
    password: str

class Register(Base_User,BaseModel):
    # _id: ObjectId
    _id: ObjectId = Field(default_factory=ObjectId, alias="_id") 
    nombre: Optional[str]
    correo: EmailStr
    password: Optional[str]
    is_active: bool = True
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None