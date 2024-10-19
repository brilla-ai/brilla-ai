from typing import Generic, TypeVar, Optional, Union
import uuid
from pydantic import BaseModel
from fastapi import status as http_status
from fastapi.responses import JSONResponse

T = TypeVar('T')

class BaseResponseModel(BaseModel, Generic[T]):
    data: Optional[T] = None
    message: Optional[str] = "Success"
    status_code: int = http_status.HTTP_200_OK

    class Config:
        from_attributes = True

    
    @staticmethod
    def create_response(data: Optional[T] = None, message: Optional[str] = "Success", status_code = http_status.HTTP_200_OK):
        

        return {
                "data": data,
                "message": message,
                "status_code": status_code
            }
        



def convert_uuids_to_str(data: Union[dict, list]):
    """
    Recursively converts UUID objects to strings in a dictionary or list.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, uuid.UUID):
                data[key] = str(value)
            elif isinstance(value, (dict, list)):
                convert_uuids_to_str(value)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, uuid.UUID):
                data[index] = str(item)
            elif isinstance(item, (dict, list)):
                convert_uuids_to_str(item)
    return data