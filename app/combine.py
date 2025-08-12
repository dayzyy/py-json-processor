from collections import defaultdict
from typing import List
from models.custom_models import Student, Room

def combine(students: List[Student], rooms: List[Room]):
    room_map = defaultdict(list)

    for s in students:
        room_map[s.room].append(vars(s))

    result = []
    for room in rooms:
        result.append({
            "id": room.id,
            "name": room.name,
            "students": room_map.get(room.id, [])
        })

    return result
