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
                    "students": [
                        {"id": 0, "name": "Luka", "room": 1},
                        {"id": 1, "name": "Vaso", "room": 1}
                    ]
                },
                {
                    "id": 2,
                    "name": "Room #2",
                    "students": [
                        {"id": 2, "name": "Deme", "room": 2}
                    ]
                }
            ]
        ),

        # No students at all
        (
            [],
            [Room(id=1, name="Room #1"), Room(id=2, name="Room #2")],
            [
                {"id": 1, "name": "Room #1", "students": []},
                {"id": 2, "name": "Room #2", "students": []}
            ]
        ),

        # No rooms at all
        (
            [Student(id=0, name="Luka", room=1)],
            [],
            []
        ),

        # Student whose `room` doesn't match any room
        (
            [Student(id=0, name="Luka", room=999)],
            [Room(id=1, name="Room #1")],
            [
                {"id": 1, "name": "Room #1", "students": []}
            ]
        ),

        # Multiple rooms, some with no students
        (
            [
                Student(id=0, name="Luka", room=1),
                Student(id=1, name="Ana", room=3)
            ],
            [
                Room(id=1, name="Room #1"),
                Room(id=2, name="Room #2"),
                Room(id=3, name="Room #3")
            ],
            [
                {"id": 1, "name": "Room #1", "students": [{"id": 0, "name": "Luka", "room": 1}]},
                {"id": 2, "name": "Room #2", "students": []},
                {"id": 3, "name": "Room #3", "students": [{"id": 1, "name": "Ana", "room": 3}]}
            ]
        ),
    ]
)
def test_combine(students: List[Student], rooms: List[Room], expected):
    assert combine(students, rooms) == expected
