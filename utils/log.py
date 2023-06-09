from typing import Optional, Any
from datetime import datetime
from pydantic import Field
from beanie import PydanticObjectId, Document
from pymongo import ASCENDING
from pymongo.operations import IndexModel


class Log(Document):
    user: Optional[PydanticObjectId]
    collection: str
    action: str
    before: Any
    after: Any
    date: datetime = Field(default_factory=datetime.today)

    class Settings:
        name = "logs"
        indexes = [
            IndexModel(
                [("user", ASCENDING)],
                name="user_ASCENDING",
            ),
            IndexModel(
                [("collection", ASCENDING)],
                name="collection_ASCENDING",
            ),
            IndexModel(
                [("action", ASCENDING)],
                name="action_ASCENDING",
            ),
            IndexModel(
                [("date", ASCENDING)],
                name="date_ASCENDING",
            ),
        ]
