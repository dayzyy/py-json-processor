from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Type, Protocol, Any
from functools import wraps

T = TypeVar('T')

class SerializerMeta(Protocol):
    model: Any
    fields: Optional[List[str]] = None
    exclude: Optional[List[str]] = None

class Serializer(ABC):
    @staticmethod
    def ensure_meta(method):
        @wraps(method)
        def wrapper(cls, *args, **kwargs):
            cls._validate_meta()

            return method(cls, *args, **kwargs)
        return wrapper

    @classmethod
    def _get_meta(cls) -> Type[SerializerMeta] | None:
        return getattr(cls, 'Meta', None)

    @classmethod
    def _get_fields(cls) -> List[str]:
        meta = cls._get_meta()
        model = meta.model
        assert model is not None

        fields = getattr(meta, 'fields', None)
        if fields:
            return fields

        fields = getattr(model, '__annotations__', {}).keys()
        exclude = getattr(meta, 'exclude') or []

        return [field for field in fields if field not in exclude]

    @classmethod
    def _validate_fields(cls, fields, model) -> None:
        for field in fields:
            if field not in model.__annotations__.keys():
                raise ValueError(f"Attribute {field!r} does not exist on class {model.__name__!r}")

    @classmethod
    def _validate_meta(cls) -> None:
        meta = cls._get_meta()

        if meta is None or not hasattr(meta, 'model'):
            raise ValueError(f"Serializer class must define a Meta class with a 'model' attribute")

        cls._validate_fields(cls._get_fields(), meta.model)

    @classmethod
    @abstractmethod
    def serialize(cls, instance: T) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def deserialize(cls, data: str) -> T:
        raise NotImplementedError
