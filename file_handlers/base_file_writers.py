from abc import ABC, abstractmethod

class BaseFileWrite(ABC):
    @classmethod
    @abstractmethod
    def write(cls, file_path: str, data: str) -> None:
        raise NotImplementedError

# Supports writing to any text formatted file (JSON, XML, CSV etc.)
class TextFileWriter(BaseFileWrite):
    @classmethod
    def write(cls, file_path: str, data: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)
