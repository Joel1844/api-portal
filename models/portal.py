from pydantic.dataclasses import dataclass
from pydantic import BaseModel,validator
from typing import Optional,List
from fastapi import Form, File, UploadFile
from bson import ObjectId
from enum import Enum


@dataclass
class Portal:
    name: str = Form(default=None)
    Lastname: str = Form(default=None)
    Titulo : str = Form(default=None) 
    fecha: str = Form(default=None)
    video: str = Form(default=None)
    imagen: str = Form(default=None)
    latitude: str = Form(default=None)
    longitude: str = Form(default=None)
    clasification: str = Form(default=None)
    description: str = Form(default=None)
    fuente : str = Form(default=None)
   

class STATUS(str, Enum):
    APROBADO = "Aprobado"
    RECHAZADO = "Rechazado"


class UpdatePortal(BaseModel):
    ids: List[str]
    status: STATUS

    @validator('ids')
    def validate_object_ids(cls, ids):
        for id in ids:
            if not ObjectId.is_valid(id):
                raise ValueError(f"ID inválido: {id}")
        return ids
