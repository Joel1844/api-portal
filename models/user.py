from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    name: str
    phone: str
    neighborhood: str
    occupation: str
    professional_level: str
    exercise: str
    age: str
    weight: str
    start_weight: str
    end_weight: str
    goal_weight: str
    disease: str
    plan: str
    height: str
    sex : str
    more_request: str
    time_plan: str
