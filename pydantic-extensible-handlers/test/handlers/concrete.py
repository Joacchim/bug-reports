from typing import Optional
import pydantic

from .base import BaseHandler

class Handler1Config(pydantic.BaseModel):
    field1: Optional[str]
    field2: Optional[int]

class Handler1(BaseHandler):
    db_type: str = 'handler_1'
    conf_key: str = 'one'
    conf_type = Handler1Config
