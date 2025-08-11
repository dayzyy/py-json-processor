from abc import ABC, abstractmethod

class BaseFileWrite(ABC):
    @classmethod
    @abstractmethod
    def write(cls, file_path: str, data: str) -> None:
        raise NotImplementedError
