from pydantic.dataclasses import  dataclass
from typing import Optional
from fastapi import Form, File, UploadFile

@dataclass
class Portal:
    # id : Optional[str]
    # id : Optional[str] = Form(None)
    name: str = Form(...)
    date: str = Form(...)
    video: str = Form(...)
    latitude: str = Form(...)
    longitude: str = Form(...)

