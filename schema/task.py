
from pydantic import BaseModel
from typing import Optional

class TaskSchema(BaseModel):
    id: Optional[str]
    name: str
    description: str
    idUser: str