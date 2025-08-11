import pytest
from models.model import Model
from contextlib import nullcontext as does_not_raise

def test_model_init_raises_for_unexpected_attribute():
    class Student(Model):
        id: int
        name: str
        room: int

    with pytest.raises(ValueError, match="Unexpected attribute 'last_name' when instantiating class 'Student'"):
        Student(id=1, name='Luka', last_name='Mania', room=111)

def test_model_init_raises_for_missing_attribute():
    class Room(Model):
        id: int
        name: str

    with pytest.raises(ValueError, match="Missing attribute 'name' when instantiating class 'Room'"):
        Room(id=1)
