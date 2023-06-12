from pydantic import BaseModel
from typing import Optional

from .handlers import HandlersConfig

class Config(BaseModel):
    handlers: Optional[HandlersConfig]
