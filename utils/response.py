import json
from typing import Any, Optional, Generic, TypeVar, Union
from fastapi import status, Response as FastAPIResponse
from pydantic.generics import GenericModel

T = TypeVar('T')


class Response(GenericModel, Generic[T]):
    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "La acción se ha realizado correctamente"
    data: Optional[T] = None


class ErrorResponse(Response[T], Generic[T]):
    success: bool = False
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Error en la acción"


class CustomResponse(FastAPIResponse):
    media_type = "application/json"

    def render(self, content: Union[Response, Any]) -> bytes:
        if isinstance(content, Response):
            return json.dumps(content.dict()).encode("utf-8")
        return json.dumps(content).encode("utf-8")
