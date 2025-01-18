from pydantic import BaseModel
from typing import List, Optional

class Material(BaseModel):
    id: str
    title: str
    description: str
    type: str
    content: str
    stage_id: str
