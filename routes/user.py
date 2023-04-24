from fastapi import APIRouter,responses,status
from fastapi.responses import JSONResponse
from config.db import CollectionRedSocial
from schemas.user import userEntity, usersEntity
from models.user import User
from bson import ObjectId

from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()


@user.get("/users",tags=["users"])
def find_all_users():
    return usersEntity(CollectionRedSocial.find())


#create post para almacenar un usuario en la base de datos
@user.post("/users",tags=["users"])
async def create_user(user: User):
    new_user = dict(user)
    del new_user["id"]
    id =  CollectionRedSocial.insert_one(new_user)
    print(id)
    user =  CollectionRedSocial.find_one({"_id": id.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=userEntity(user))
    
@user.get("/users/{id}",tags=["users"])
def find_user(id: str):
    return userEntity(CollectionRedSocial.find_one({"_id": ObjectId(id)}))

@user.put("/users/{id}",tags=["users"])
def update_user(id: str, user: User):
    new_user = dict(user)
    del new_user["id"]
    CollectionRedSocial.update_one({"_id": ObjectId(id)}, {"$set": new_user})
    user = CollectionRedSocial.find_one({"_id": ObjectId(id)})
    return userEntity(user)


@user.delete("/users/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=["users"])
def delete_users(id: str):
    userEntity(CollectionRedSocial.find_one_and_delete({"_id": ObjectId(id)}))
    return responses.Response(status_code=HTTP_204_NO_CONTENT)