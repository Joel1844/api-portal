from fastapi import APIRouter,responses,status,UploadFile,File,Form,Depends
from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from config.db import collectionportal, colletionvideo
from schemas.portal import portalEntity, portalsEntity
from models.portal import Portal
from bson import ObjectId
from fastapi.responses import FileResponse
import os 

from starlette.status import HTTP_204_NO_CONTENT

portal = APIRouter()


@portal.get("/portal",tags=["portal"])
def find_all_users():
    return portalsEntity(collectionportal.find())

@portal.post("/portal", tags=["portal"])
async def create_user(portal: Portal = Depends(), video_file: UploadFile = File(...)):
    video_content = await video_file.read() # leer el contenido del archivo
    carpeta = ("VIOLENCIA")
    contenido_archivo = video_content
    video_id = colletionvideo.insert_one({"description": video_file.filename}).inserted_id
    os.makedirs(carpeta, exist_ok=True)
    rutacompleta = os.path.join(carpeta, f"{str(video_id)}.{video_file.content_type.split('/')[1]}")


    with open(rutacompleta, 'wb') as f:
        print(rutacompleta)
        # escribir los datos binarios en el archivo
        f.write(contenido_archivo)
    
    f.close() # cerrar la conexión con el servidor de archivos

    new_portal = {"name": portal.name, "date": portal.date, "video": str(rutacompleta), "latitude": portal.latitude, "longitude": portal.longitude, "status": "Pendiente"}
    # del new_portal["id"]
    id = collectionportal.insert_one(new_portal)
    portal =  collectionportal.find_one({"_id": id.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=portalEntity(portal))


# @portal.post("/upload-video/")
# async def upload_video(video_file: UploadFile = File(...)):
#     video_content = await video_file.read() # leer el contenido del archivo

#     carpeta = ("VIOLENCIA")
#     nomrbe_archivo = video_file.filename
#     contenido_archivo = video_content

#     video_id = colletionvideo.insert_one({"description": video_file.filename}).inserted_id
#     os.makedirs(carpeta, exist_ok=True)
#     rutacompleta = os.path.join(carpeta, f"{str(video_id)}.{video_file.content_type.split('/')[1]}")


#     with open(rutacompleta, 'wb') as f:
#         print(rutacompleta)
#         # escribir los datos binarios en el archivo
#         f.write(contenido_archivo)
    
#     f.close() # cerrar la conexión con el servidor de archivos

#     return {"message": f"{video_id}"}



@portal.get("/archivo/{nombre_archivo}")
async def get_archivo(nombre_archivo: str):
    return FileResponse(f"VIOLENCIA/{nombre_archivo}.mp4")





# @portal.post("/portal/",tags=["portal"])
# async def create_user(portal: Portal, video_file: UploadFile = File(...)):
    
#     video_content = await video_file.read()
#     carpeta = ("VIOLENCIA")
#     nomrbe_archivo = video_file.filename
#     contenido_archivo = video_content
#     os.makedirs(carpeta, exist_ok=True)
#     rutacompleta = os.path.join(carpeta, nomrbe_archivo)
#     with open(rutacompleta, 'wb') as f:
#         f.write(contenido_archivo)

    
#     new_portal = dict(portal)
#     del new_portal["id"]
#     id = collectionportal.insert_one(new_portal)
#     portal = collectionportal.find_one({"_id": id.inserted_id})
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=portalEntity(portal))

#    new_portal = dict(portal)
#     del new_portal["id"]
#     id = collectionportal.insert_one(new_portal)
#     portal = collectionportal.find_one({"_id": id.inserted_id})
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=portalEntity(portal))