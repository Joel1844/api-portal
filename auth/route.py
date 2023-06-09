from urllib import request

from fastapi import FastAPI, Form,Response
from fastapi import APIRouter, BackgroundTasks
from dotenv import load_dotenv
from os import getenv

router = APIRouter()
load_dotenv()

from ..config.db import DbRed

from ..auth.auth_model import Login,Register
from fastapi import FastAPI, HTTPException, Depends, Request,status
# from utils import *
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt

import os

from dotenv import load_dotenv

load_dotenv()

# from oauth import get_current_user


# from jwttoken import create_access_token

from ..token.jwtToken import create_access_token

from fastapi.security import OAuth2PasswordRequestForm

# from hashing import Hash
from ..token.hashing import Hash

from .auth_model import Base_User

from .oauth import get_current_user

collection =  DbRed["users"]

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

@router.get("/")
def read_root(current_user:Login = Depends(get_current_user)):
	return {"data":"Hello OWrld"}

@router.post("/login")
async def login_user(request:Login):

    try:
        
        user = await DbRed["users"].find_one({"correo": request.correo})

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")

        if not Hash.verify(user['password'] ,request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrect password")

        access_token = create_access_token(data={"sub": user["correo"]})

        return {'message': 'Logueado con exito.',"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        return str(e)



@router.post("/register", summary="create new users")
async def register_user(user: Register):
    user_db = DbRed["users"]

    print(Register)
    # user_db = await database["users"].insert_one(user.dict())
    exist = await user_db.find_one({"correo": user.correo})
    print(exist)
    if exist:
        print(user_db)
        return {"message": "El usuario ya existe"}
    else:
        hashed_pass = Hash.bcrypt(user.password)
        user_object = dict(user)
        user_object["password"] = hashed_pass
        # user_id = database["users"].insert(user_object)
        inserted = await user_db.insert_one(user_object)

        return str(inserted.inserted_id) and {"res":"created"}

        # inserted = await user_db.insert_one(user.dict())
        # return  str(inserted.inserted_id)