from fastapi import APIRouter, FastAPI, Request,status,UploadFile,File,Depends, HTTPException,Query
from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from config.db import collectionportal, colletionvideo, collentioninsta,collentionlistim
from schemas.portal import portalEntity, portalsEntity, instagramEsEntity, diarioEsEntity
from models.portal import Portal,UpdatePortal
from fastapi.responses import FileResponse
import os 
import math
from math import ceil
from pymongo.errors import DuplicateKeyError

from dotenv import load_dotenv
from bson import ObjectId

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
    status: Optional[str] = Query(None)
):
    query = {}

    if page is not None and page < 1:
        raise HTTPException(status_code=400, )

    if limit is not None and (limit not in [10, 25, 100]):
        raise HTTPException(status_code=400)

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
    
    actual_page = page if page is not None else 1


    response = {
        "total_pages": total_pages,
        "data": portalsEntity(results),
        
    }

    return response

@portal.get("/portal/exporta", tags=["portal"])
def fill_all_users():
    return portalsEntity(collectionportal.find())
    

@app.exception_handler(DuplicateKeyError)
async def handle_duplicate_key_error(request, exc):
    error_message = "Clave duplicada"
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": error_message})

@app.exception_handler(HTTPException)
async def handle_http_exception(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

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
            #hacer que la fecha vengan deun formato correcto    
            "fecha": portal.fecha,
            "video": api_url_video if guardarvideo is not None else None,
            "imagen": apir_url_imagen if guardarimagen is not None else None,
            "latitude": portal.latitude, 
            "longitude": portal.longitude,
            "clasificacion": portal.clasification,
            "descripcion": portal.description,
            "status": "Pendiente",
            "Titulo": portal.Titulo,
            "fuente": portal.fuente,
            'url:': "no tiene",
        }

        if new_portal["video"] is None and new_portal["imagen"] is None:
            raise HTTPException(status_code=400, detail="At least one of 'video' or 'imagen' is required.")

        id = collectionportal.insert_one(new_portal)
        portal = collectionportal.find_one({"_id": id.inserted_id})

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=portalEntity(portal))
    
    except DuplicateKeyError:
        error_message = "Clave duplicada"
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": error_message})
    
    except Exception as error:
        # Si ocurre un error diferente a DuplicateKeyError, no se guardarán los archivos
        error_message = str(error)
        raise HTTPException(status_code=500, detail=error_message)
    



@portal.get("/instagraminfo/", tags=["portal"])
def find_all_users2():
    date = collentioninsta.find()
    return instagramEsEntity(collentioninsta.find())


#acrualizar el status de la base de datos mediante el id
@portal.put("/portal", tags=["portal"])
def actualizar_status(body: UpdatePortal):

    ids = [ObjectId(id) for id in body.ids]

    collectionportal.update_many({"_id": {'$in': ids}}, {"$set": {"status": body.status}})

    #devolver los datos actualizados 
    return portalsEntity(collectionportal.find({"_id": {'$in': ids}}))


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

@portal.get("/archivovideo/{nombre_archivo}")
async def get_archivo(nombre_archivo: str):
    return FileResponse(f"VIOLENCIA/{nombre_archivo}")


@portal.get("/archivovimagen/{nombre_archivo}")
async def get_archivo(nombre_archivo: str):
    return FileResponse(f"VIOIMAGEN/{nombre_archivo}")
