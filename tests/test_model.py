import pytest
from models.model import Model
from contextlib import nullcontext as does_not_raise

def test_model_init_raises_for_unexpected_attribute():
    class Student(Model):
        id: int
        name: str
        room: int

    with pytest.raises(ValueError, match="Unexpected attribute 'last_name' while instantiating class 'Student'"):
        Student(id=1, name='Luka', last_name='Mania', room=111)
