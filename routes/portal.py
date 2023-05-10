from fastapi import APIRouter, Request,responses,status,UploadFile,File,Form,Depends
from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from config.db import collectionportal, colletionvideo, collentioninsta
from schemas.portal import portalEntity, portalsEntity, instagramEntity, instagramEsEntity
from models.portal import Portal
from bson import ObjectId
from fastapi.responses import FileResponse
import os 
import requests
import pytube
import instaloader

from starlette.status import HTTP_204_NO_CONTENT

portal = APIRouter()


@portal.get("/portal",tags=["portal"])
def find_all_users():
    return portalsEntity(collectionportal.find())

@portal.post("/portal", tags=["portal"])
async def create_user(req:Request ,portal: Portal = Depends(), video_file: UploadFile = File(...), ):
    video_content = await video_file.read() # leer el contenido del archivo
    carpeta = ("VIOLENCIA")
    contenido_archivo = video_content
    video_id = colletionvideo.insert_one({"description": video_file.filename}).inserted_id
    os.makedirs(carpeta, exist_ok=True)
    rutacompleta = os.path.join(carpeta, f"{str(video_id)}.{video_file.content_type.split('/'   )[1]}")
    guardarvideo = f"{req.base_url}archivo/{video_id}"
    

    with open(rutacompleta, 'wb') as f:
        print(rutacompleta)
        # escribir los datos binarios en el archivo
        f.write(contenido_archivo)
    
    f.close() #

    new_portal = {"name": portal.name, "date": portal.date, "video": guardarvideo, "latitude": portal.latitude, "longitude": portal.longitude, "status": "Pendiente"}
    # del new_portal["id"]
    id = collectionportal.insert_one(new_portal)
    portal =  collectionportal.find_one({"_id": id.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=portalEntity(portal))



@portal.get("/instagraminfo/", tags=["portal"])
def find_all_users2():
    return instagramEsEntity(collentioninsta.find())


@portal.post("/instagraminfo/", tags=["portal"])
async def create_user2(url: str):
    response = requests.get(url)
    html = response.text
    L = instaloader.Instaloader()
    # Encuentra el enlace de descarga del video y la información del post
    shortcode = url.split("/")[-2]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    video_url = url
    title = post.caption
    date = post.date
    owner_username = post.owner_username

    new_scrape = {"title": title, "date": str(date), "video": video_url, "owner_username": owner_username, "status": "Pendiente", 'fuente': 'instagram'}
    # del new_portal["id"]
    id = collentioninsta.insert_one(new_scrape)
    new_scrape =  collentioninsta.find_one({"_id": id.inserted_id})
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=instagramEntity(new_scrape))

@portal.post("/youtubeinfo/", tags=["portal"])
async def create_user3(url: str):
# Create a PyTube YouTube object
    yt = pytube.YouTube(url)

    # Get the video title and publish date
    video_title = yt.title
    video_publish_date = yt.publish_date
    owner_username = yt.author

    # Check if the video is a stream or an adaptive stream
    if yt.streams.first().type == "video":
        # Video stream
        video_url = yt.streams.first().url
    else:
        # Adaptive stream
        video_url = yt.streams.filter(progressive=True).order_by('resolution').desc().first().url

    new_scrape = {"title": video_title, "date": str(video_publish_date), "video": video_url, "owner_username": owner_username, "status": "Pendiente", 'fuente': 'youtube'}
    # del new_portal["id"]
    id = collentioninsta.insert_one(new_scrape)
    new_scrape =  collentioninsta.find_one({"_id": id.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=instagramEntity(new_scrape))


@portal.get("/archivo/{nombre_archivo}")
async def get_archivo(nombre_archivo: str):
    return FileResponse(f"VIOLENCIA/{nombre_archivo}.mp4")




