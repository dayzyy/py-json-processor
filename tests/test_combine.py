from typing import List
import pytest
from models.custom_models import Student, Room
from app.combine import combine

@pytest.mark.parametrize(
    'students,rooms,expected',
    [
        (
            [
                Student(id=0, name="Luka", room=1),
                Student(id=1, name="Vaso", room=1),
                Student(id=2, name="Deme", room=2)
            ],
            [
                Room(id=1, name="Room #1"),
                Room(id=2, name="Room #2")
            ],
            [
                {
                    "id": 1, 
                    "name": "Room #1",
                    "students": [{"id": 0, "name": "Luka", "room": 1}, {"id": 1, "name": "Vaso", "room": 1}]
                },
                {
                    "id": 2, 
                    "name": "Room #2",
                    "students": [{"id": 2, "name": "Deme", "room": 2}]
                }
            ]
        )
    ]
)
def test_combine(students: List[Student], rooms: List[Room], expected):
    assert combine(students, rooms) == expected
