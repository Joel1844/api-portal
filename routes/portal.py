from fastapi import APIRouter, Request,responses,status,UploadFile,File,Form,Depends, HTTPException
from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from config.db import collectionportal, colletionvideo, collentioninsta,collentionlistim
from schemas.portal import portalEntity, portalsEntity, instagramEntity, instagramEsEntity, diarioEntity, diarioEsEntity
from models.portal import Portal
from bson import ObjectId
from fastapi.responses import FileResponse
import os 
import requests
import pytube
import instaloader



from dotenv import load_dotenv

load_dotenv()


from datetime import datetime
import requests
import time 

from starlette.status import HTTP_204_NO_CONTENT

portal = APIRouter()


@portal.get("/portal",tags=["portal"])
def find_all_users():
    return portalsEntity(collectionportal.find())

@portal.post("/portal", tags=["portal"])
async def create_user(req:Request ,portal: Portal = Depends(), video_file: Optional[UploadFile]= File(default=None),image_file: Optional[UploadFile] = File(default=None) ):

    carpeta = "VIOLENCIA"
    os.makedirs(carpeta, exist_ok=True)

    video_id = None
    guardarvideo = None
    if video_file is not None:
        video_content = await video_file.read()
        video_id = colletionvideo.insert_one({"description": video_file.filename}).inserted_id
        video_rutacompleta = os.path.join(carpeta, f"{str(video_id)}.{video_file.content_type.split('/')[1]}")
        
        with open(video_rutacompleta, 'wb') as f:
            f.write(video_content)
        
        guardarvideo = f"{req.base_url}VIOLENCIA/{video_id}"
    
    image_id = None
    guardarimagen = None
    if image_file is not None:
        image_content = await image_file.read()
        image_id = colletionvideo.insert_one({"description": image_file.filename}).inserted_id
        image_rutacompleta = os.path.join(carpeta, f"{str(image_id)}.{image_file.content_type.split('/')[1]}")
        
        with open(image_rutacompleta, 'wb') as f:
            f.write(image_content)

        guardarimagen = f"{req.base_url}VIOLENCIA/{image_id}"

    new_portal = {
        "name": portal.name,
        "date": portal.date,
        "video": guardarvideo if guardarvideo is not None else None,
        "image": guardarimagen if guardarimagen is not None else None,
        "latitude": portal.latitude, 
        "longitude": portal.longitude,
        "clasificacion": portal.clasification,
        "descripcion": portal.description,
        "status": "Pendiente"
    }

    if new_portal["video"] is None and new_portal["image"] is None:
        raise HTTPException(status_code=400, detail="At least one of 'video' or 'image' is required.")

    # if guardarvideo is not None:
    #     new_portal["video"] = guardarvideo
    
    # if guardarimagen is not None:
    #     new_portal["image"] = guardarimagen

    id = collectionportal.insert_one(new_portal)
    portal = collectionportal.find_one({"_id": id.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=portalEntity(portal))


@portal.get("/instagraminfo/", tags=["portal"])
def find_all_users2():
    date = collentioninsta.find()
    return instagramEsEntity(collentioninsta.find())


# @portal.post("/instagraminfo/", tags=["portal"])
# async def create_user2(url: str):
#     response = requests.get(url)
#     html = response.text
#     L = instaloader.Instaloader()
#     # Encuentra el enlace de descarga del video y la información del post
#     shortcode = url.split("/")[-2]
#     post = instaloader.Post.from_shortcode(L.context, shortcode)
#     video_url = url
#     title = post.caption
#     date = post.date,
#     imagen = post.url

#     date  = date.strftime("%d/%m/%Y")
#     owner_username = post.owner_username


#     new_scrape = {"Nombre": title, "fecha": str(date), "video": video_url, "owner_username": owner_username, "status": "Pendiente", 'fuente': 'instagram', "imagen": imagen}
#     # del new_portal["id"]
#     id = collentioninsta.insert_one(new_scrape)
#     new_scrape =  collentioninsta.find_one({"_id": id.inserted_id})
    
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=instagramEntity(new_scrape))

# @portal.post("/youtubeinfo/", tags=["portal"])
# async def create_user3(url: str):
# # Create a PyTube YouTube object
#     yt = pytube.YouTube(url)

#     # Get the video title and publish date
#     video_title = yt.title
#     video_publish_date = yt.publish_date
#     video_publish_date = video_publish_date.strftime("%d/%m/%Y")
#     owner_username = yt.author

#     # Check if the video is a stream or an adaptive stream
#     if yt.streams.first().type == "video":
#         # Video stream
#         video_url = yt.streams.first().url
#     else:
#         # Adaptive stream
#         video_url = yt.streams.filter(progressive=True).order_by('resolution').desc().first().url

#     new_scrape = {"Nombre": video_title, "fecha": str(video_publish_date), "video": video_url, "owner_username": owner_username, "status": "Pendiente", 'fuente': 'youtube', "imagen": "https://www.youtube.com/img/desktop/yt_1200.png"}
#     # del new_portal["id"]
#     id = collentioninsta.insert_one(new_scrape)
#     new_scrape =  collentioninsta.find_one({"_id": id.inserted_id})

#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=instagramEntity(new_scrape))


#make scrape diario libre 
# @portal.post("/listininfo/", tags=["portal"])


@portal.get("/listininfo/", tags=["portal"])
def find_all_users3():
    return diarioEsEntity(collentionlistim.find())

@portal.get("/archivo/{nombre_archivo}")
async def get_archivo(nombre_archivo: str):
    return FileResponse(f"VIOLENCIA/{nombre_archivo}.mp4")

#listar todos los videos que vienen de la carpeta VIOLENCIA 
@portal.get("/listarvideos/", tags=["portal"])
def find_all_users4():
    return listvideosEntity(collentionvideo.find())





