from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any, Optional

from .factory import Factory

class BaseHandler(ABC):
    db_type: str = '__base__'
    conf_key: str = ''
    conf_type: type[BaseModel]

    def __init_subclass__(cls, **kwargs):
        """
        Automatically registers any subclass into the Factory
        """
        print(f'Initializing subclass for {cls.db_type}')
        Factory._register(cls)
        if cls.db_type == '__base__':
            raise TypeError(
                'BaseHandler child classes must specify a valid db_type class-attribute value'
            )
        if not cls.conf_key:
            raise TypeError(
                'BaseHandler child classes must specify a valid conf_key class-attribute value'
            )
        if cls.conf_type is None:
            raise TypeError(
                'BaseHandler child classes must specify a valid conf_type class-attribute value'
            )

    def __init__(self, conf: Optional[BaseModel] = None) -> None:
        ...

    @abstractmethod
    def eligible(self, job_md: dict[str, Any]) -> bool:
        ...

    @abstractmethod
    def acquire(self, job_md: dict[str, Any], strict: bool = True) -> None:
        ...

    @abstractmethod
    def release(self, job_md: dict[str, Any], strict: bool = True) -> None:
        ...
