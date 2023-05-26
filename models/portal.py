from pydantic.dataclasses import  dataclass
from typing import Optional
from fastapi import Form, File, UploadFile

@dataclass
class Portal:
    # id : Optional[str]
    # id : Optional[str] = Form(None)
    name: str = Form(default=None)
    Lastname: str = Form(default=None)
    titulo : str = Form(default=None) 
    fecha: str = Form(default=None)
    video: str = Form(default=None)
    imagen: str = Form(default=None)
    latitude: str = Form(default=None)
    longitude: str = Form(default=None)
    clasification: str = Form(default=None)
    description: str = Form(default=None)
    fuente : str = Form(default=None)
   
    

