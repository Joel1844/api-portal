from beanie import Document, PydanticObjectId, Insert, Replace, Delete, before_event, after_event
from typing import Optional
from typing_extensions import Self
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel
from .log import Log


class BaseFields(BaseModel):
    create_at: Optional[datetime]
    create_by: Optional[PydanticObjectId]
    update_at: Optional[datetime]
    update_by: Optional[PydanticObjectId]


class Base(Document):
    create_at: Optional[datetime]
    create_by: Optional[PydanticObjectId]
    update_at: Optional[datetime]
    update_by: Optional[PydanticObjectId]

    @after_event(Insert)
    async def set_create_at(self):
        log = Log(user=self.create_by, collection=self.get_collection_name(),
                  action="insert_one", before=None, after=self)
        await log.insert()

    @before_event(Replace)
    async def set_update_current(self):
        if self.id:
            before = await self.get(self.id)
            log = Log(user=self.update_by, collection=self.get_collection_name(),
                      action="update_one", before=before, after=self)
            await log.insert()

    @after_event(Delete)
    async def set_delete_at(self):
        log = Log(user=self.update_by, collection=self.get_collection_name(),
                  action="delete_one", before=self, after=None)
        await log.insert()


class ModelAdmin(Base):
    @classmethod
    async def find_by_id(cls, id: PydanticObjectId) -> Self:
        found = await cls.get(id)
        if not found:
            raise HTTPException(
                status_code=404, detail="Recurso no encontrado")
        return found

    @classmethod
    async def insert_one(cls, data: Base, user_id: PydanticObjectId):
        data.create_by = user_id
        data.create_at = datetime.now()
        await data.insert()
        return data

    @classmethod
    async def update_one(cls, id: PydanticObjectId, query: dict, user_id: PydanticObjectId):
        found = await cls.find_by_id(id)
        update_info = {'update_by': user_id, 'update_at': datetime.now()}
        set_query = query.get("$set", {})
        query["$set"] = {**set_query, **update_info}
        await found.update(query)
        await found.replace()
        return found

    @classmethod
    async def delete_one(cls, id: PydanticObjectId, user_id: PydanticObjectId):
        found = await cls.find_by_id(id)
        found.update_by = user_id
        found.update_at = datetime.now()
        await found.delete()
        return found
