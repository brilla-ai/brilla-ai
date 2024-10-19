

import json
from typing import Type, Any, List, Union

from pydantic import BaseModel


def apply_pydantic_model(pydantic_class: Type[BaseModel], data: Union[Any, List[Any]]) -> Union[BaseModel, List[BaseModel]]:
    """
    Helper function to apply the Pydantic model to the given data or list of data.

    Args:
        pydantic_class (Type[BaseModel]): The Pydantic model class to apply.
        data (Any | List[Any]): The data to convert, either a single object or a list of objects.

    Returns:
        BaseModel | List[BaseModel]: An instance or list of instances of the Pydantic model with data applied.
    """
    if isinstance(data, list):
        # Convert each item in the list to a dict and apply Pydantic model
        
        response  =  [pydantic_class(**item.__dict__) for item in data]
        return json.dumps(response)
    else:
        # Convert single SQLAlchemy object to a dict and apply Pydantic model
        return pydantic_class(**data.__dict__).model_dump_json()

