import pytest
from models.model import Model
from contextlib import nullcontext as does_not_raise

def test_model_init_sets_instance_attributes_via_class_annotations():
    class Student(Model):
        id: int
        name: str
        room: int

    student = Student(id=1, name='Luka', room=111)

    assert getattr(student, 'id', None) == 1
    assert getattr(student, 'name', None) == 'Luka'
    assert getattr(student, 'room', None) == 111

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

    with pytest.raises(ValueError, match=r"Missing attribute \['name'\] when instantiating class 'Room'"):
        Room(id=1)

def test_model_init_raises_for_attribute_type_missmatch():
    class Student(Model):
        id: int
        name: str
        room: int

    with pytest.raises(ValueError, match="Invalid type for attribute 'room' when instantiating class 'Student': expected 'int', got 'str'"):
        Student(id=1, name='Luka', room="bathroom")
