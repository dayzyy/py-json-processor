from models.base_models import Model

class Student(Model):
    id: int
    name: str
    room: int

class Room(Model):
    id: int
    name: str
