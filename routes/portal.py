from fastapi import APIRouter, FastAPI, Request,status,UploadFile,File,Depends, HTTPException,Query
from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from config.db import collectionportal, colletionvideo, collentioninsta,collentionlistim
from schemas.portal import portalEntity, portalsEntity
from models.portal import Portal,UpdatePortal
from fastapi.responses import FileResponse
import os 
import math
from math import ceil
from pymongo.errors import DuplicateKeyError

import instaloader
import requests
from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime

load_dotenv()


from datetime import datetime

import time 

from starlette.status import HTTP_204_NO_CONTENT

portal = APIRouter()

app = FastAPI()


from math import ceil

#aquii se hace la consulta de la base de datos
@portal.get("/portal", tags=["portal"])
def find_all_users(
    page: Optional[int] = Query(1, ge=1),
    limit: Optional[int] = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),

):


    query = {}

    if search is not None:
        query["Titulo"] =  { "$regex": diacritic_sensitive(search), "$options": "i" }

    if page is not None and page < 1:
        raise HTTPException(status_code=400, )

    if status is not None:
        query["status"] = status

    total_documents = collectionportal.count_documents(query)

    if page is not None and limit is not None:
        skip_count = (page - 1) * limit
        data = collectionportal.find(query).skip(skip_count).limit(limit)
    else:
        data = collectionportal.find(query)

    results = list(data)

    total_pages = ceil(total_documents / limit)
    # hacer que lleguen los ultimos datos primero
    results.reverse()
    
    actual_page = page if page is not None else 1


    response = {
        "total_pages": total_pages,
        "count": total_documents,
        "data": portalsEntity(results),
        
    }

    return response



def diacritic_sensitive(text: str) -> str:
    """Add diacritics to regex"""
    return text.lower().translate(str.maketrans(
        {
            'a': '[aá]',
            'e': '[eé]',
            'i': '[ií]',
            'o': '[oó]',
            'u': '[uúü]',
            # 'ñ': '[nñ]',
        }
    ))

@portal.get("/portal/exporta", tags=["portal"])
def fill_all_users():
    return portalsEntity(collectionportal.find())
    

@app.exception_handler(DuplicateKeyError)
async def handle_duplicate_key_error(request, exc):
    error_message = "Clave duplicada"
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": error_message})

@portal.post("/portal", tags=["portal"])
async def create_user(req:Request ,portal: Portal = Depends(), video_file: Optional[UploadFile]= File(default=None),image_file: Optional[UploadFile] = File(default=None) ):

    try:
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
            
            
            guardarvideo = os.path.join(f"{carpeta}/{video_id}.{video_file.content_type.split('/')[1]}")
            api_url_video = os.path.join(f"archivovideo/{video_id}.{video_file.content_type.split('/')[1]}")
            
        
        carpeta1 = "VIOIMAGEN"
        os.makedirs(carpeta1, exist_ok=True)
        image_id = None
        guardarimagen = None
        if image_file is not None:
            image_content = await image_file.read()
            image_id = colletionvideo.insert_one({"description": image_file.filename}).inserted_id
            image_rutacompleta = os.path.join(carpeta1, f"{str(image_id)}.{image_file.content_type.split('/')[1]}")
            
            with open(image_rutacompleta, 'wb') as f:
                f.write(image_content)

            guardarimagen =os.path.join(f"{carpeta1}/{image_id}.{image_file.content_type.split('/')[1]}")
            apir_url_imagen =os.path.join(f"archivovimagen/{image_id}.{image_file.content_type.split('/')[1]}")


        new_portal = {
            "name": portal.name,
            "Lastname": portal.Lastname, 
            "fecha": portal.fecha,
            "video": api_url_video if guardarvideo is not None else None,
            "imagen": apir_url_imagen if guardarimagen is not None else None,
            "latitude": portal.latitude, 
            "longitude": portal.longitude,
            "clasificacion": portal.clasification,
            "descripcion": portal.description,
            "status": "Pendiente",
            "Titulo": portal.titulo,
            "fuente": portal.fuente,
            'url:': "https://defensordelpueblo.gob.do/",
        }

        if new_portal["video"] is None and new_portal["imagen"] is None:
            raise HTTPException(status_code=400, detail="At least one of 'video' or 'imagen' is required.")


        id = collectionportal.insert_one(new_portal)
        portal = collectionportal.find_one({"_id": id.inserted_id})

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=portalEntity(portal))
    
    except DuplicateKeyError:
        error_message = "Clave duplicada"
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": error_message})
    




#acrualizar el status de la base de datos mediante el id
@portal.put("/portal", tags=["portal"])
def actualizar_status(body: UpdatePortal):

    ids = [ObjectId(id) for id in body.ids]

    collectionportal.update_many({"_id": {'$in': ids}}, {"$set": {"status": body.status}})

    #devolver los datos actualizados 
    return portalsEntity(collectionportal.find({"_id": {'$in': ids}}))


@portal.post("/instagraminfo/", tags=["portal"])
async def create_user2(url: str):
    response = requests.get(url)
    html = response.text
    L = instaloader.Instaloader()
    # Encuentra el enlace de descarga del video y la información del post
    shortcode = url.split("/")[-2]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    urls = url 
    titulo = post.caption
    date = post.date,
    imagen = post.url

    carpetaimagen = "VIOIMAGEN"
    os.makedirs(carpetaimagen, exist_ok=True)
    image_id = None
    guardarimagen = None
    if imagen is not None:
        image_content = requests.get(imagen).content
        image_id = colletionvideo.insert_one({"description": imagen}).inserted_id
        image_rutacompleta = os.path.join(carpetaimagen, f"{str(image_id)}.jpg")
        download = open(image_rutacompleta, "wb")
        download.write(image_content)
        download.close()
        guardarimagen =os.path.join(f"{carpetaimagen}/{image_id}.jpg")
        apir_url_imagen =os.path.join(f"archivovimagen/{image_id}.jpg")

    fuente = "instagram"
    description = post.caption
    clasification = "Violencia"
    owner_username = post.owner_username
    Lastname = post.owner_username


    new_scrape = {"name": owner_username,
            "Lastname": Lastname,  
            "fecha": str(date),
            "video": None,
            "imagen": apir_url_imagen if guardarimagen is not None else None,
            "latitude": None,
            "longitude": None,
            "clasificacion": clasification,
            "descripcion": description,
            "status": "Pendiente",
            "Titulo": titulo,
            "fuente": fuente,
            'url:': urls}
    id = collectionportal.insert_one(new_scrape)
    new_s =  collectionportal.find_one({"_id": id.inserted_id})
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=portalEntity(new_s))


@portal.get("/archivovideo/{nombre_archivo}")
async def get_archivo(nombre_archivo: str):
    return FileResponse(f"VIOLENCIA/{nombre_archivo}")


@portal.get("/archivovimagen/{nombre_archivo}")
async def get_archivo(nombre_archivo: str):
    return FileResponse(f"VIOIMAGEN/{nombre_archivo}")
