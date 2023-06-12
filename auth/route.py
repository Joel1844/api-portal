
from fastapi import Form
from fastapi import APIRouter

import auth.oauth as au
import auth.auth_model as auth_model
from fastapi import HTTPException, Depends,status
from fastapi.encoders import jsonable_encoder

from token_controller import hashing, refreshToken
from .oauth import get_current_user
import os
# from ..token.hashing import Hash
# import config.db as db_config

from config.db import DbRed
router = APIRouter()
collection =  DbRed["users"]

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

@router.get("/")
def read_root(current_user:auth_model.Login = Depends(get_current_user)):
	return {"data":"Hello OWrld"}

@router.post("/login")
async def login_user(request:auth_model.Login):

    try:
        
        user = collection.find_one({"correo": request.correo})

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")

        if not hashing.Hash.verify(user['password'] ,request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrect password")

        access_token = refreshToken.create_access_token(data={"sub": user["correo"]})

        return {'message': 'Logueado con exito.',"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        return str(e)

@router.post("/register", summary="create new users")
async def register_user(user: auth_model.Register):
    user_db = collection

    try:
    
        exist = user_db.find_one({"correo": user.correo})
        print(exist)

        if exist is not None:
            return {"message": "El usuario ya existe"}
        else:

            hashed_pass = hashing.Hash.bcrypt(user.password)
            user_object = dict(user)
            user_object["password"] = hashed_pass
            # user_id = database["users"].insert(user_object)
            inserted = user_db.insert_one(user_object)

            return str(inserted.inserted_id) and {"res":"created"}
        
    except Exception as e:
        return str(e)

    # user_db = await database["users"].insert_one(user.dict())
    exist = await user_db.find_one({"correo": user.correo})
    print(exist)

    if exist is not None:
        print(user_db)
        return {"message": "El usuario ya existe"}
    else:
        hashed_pass = token_controller.hashing.Hash.bcrypt(user.password)
        user_object = dict(user)
        user_object["password"] = hashed_pass
        # user_id = database["users"].insert(user_object)
        inserted = await user_db.insert_one(user_object)

        return str(inserted.inserted_id) and {"res":"created"}

        # inserted = await user_db.insert_one(user.dict())
        # return  str(inserted.inserted_id)