from typing import Optional
from pydantic import Field, BaseModel
from pymongo.collection import Collection

import datetime


class Solicita(BaseModel):
    __collection__ = 'Solicita'

    fecha_solicitud: Optional[datetime.datetime]