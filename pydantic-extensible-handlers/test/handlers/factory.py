from typing import TYPE_CHECKING, Optional, Any

from pydantic import BaseModel
from pydantic.fields import ModelField

# Avoid cycling imports by default, since base relies on factory
if TYPE_CHECKING:
    from .base import BaseHandler


class RegistrableModel(BaseModel):

    @classmethod
    def add_fields(cls, **field_definitions: Any):
        new_fields: dict[str, ModelField] = {}

        for f_name, f_def in field_definitions.items():
            if f_name in cls.__fields__:
                raise TypeError(
                    f'Cannot register a configuration key twice. {f_name} already exists in {cls.__name__}'
                )
            if isinstance(f_def, tuple):
                try:
                    f_annotation, f_value = f_def
                except ValueError as e:
                    raise Exception(
                        'field definitions should either be a tuple of (<type>, <default>) or just a '
                        'default value, unfortunately this means tuples as '
                        'default values are not allowed'
                    ) from e
            else:
                f_annotation, f_value = None, f_def

            new_fields[f_name] = ModelField.infer(
                name=f_name,
                value=f_value,
                annotation=f_annotation,
                class_validators=None,
                config=cls.__config__,
            )

        cls.__fields__.update(new_fields)


class HandlersConfig(RegistrableModel):
    ...


HandlersGenerator = dict[str, type['BaseHandler']]


class Factory:
    types: HandlersGenerator = {}

    def __init__(self, conf: Optional[HandlersConfig] = None) -> None:
        self._conf = conf or HandlersConfig()

    def new(self, key: str) -> 'BaseHandler':
        if key not in self.types:
            raise Exception(f'No such handler: {key}')
        handler = self.types[key]
        subconf = getattr(self._conf, handler.conf_key, None)
        return handler(subconf)

    @classmethod
    def _register(cls, obj_type: type['BaseHandler']) -> None:
        if obj_type.db_type in cls.types:
            raise TypeError(
                f'A Handler is already registered for type={obj_type.db_type}'
            )
        cls.types[obj_type.db_type] = obj_type
        fields = {obj_type.conf_key: (
            Optional[obj_type.conf_type], obj_type.conf_type(),
        )}
        HandlersConfig.add_fields(**fields)
        print(f'Registered handler for {obj_type.db_type}')
