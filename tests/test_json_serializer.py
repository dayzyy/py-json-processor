from typing import List, Optional
import pytest
from serializers.base_serializers import Serializer, SerializerMeta, JSONSerializer
import json
from contextlib import nullcontext as does_not_raise

@pytest.mark.parametrize(
    'model,fields,exclude,json_data',
    [
        (
            type('Person', (), {'name': str, 'age': int}),
            None, None,
            '{"name": "Luka", "age": 20}'
        ),
        (
            type('Student', (), {'id': int, 'name': str, 'room': int}),
            None, None,
            '{"id": 0, "name": "Luka", "room": 111}'
        ),
        (
            type('Room', (), {'id': int, 'name': str}),
            None, None,
            '{"id": 19, "name": "Room #19"}'
        )
    ]
)
def test_json_serializer_serialize_and_deserialize_methods(model, fields: Optional[List[str]], exclude: Optional[List[str]], json_data: str):
    class CustomJSONSerializer(JSONSerializer):
        class Meta(SerializerMeta):
            model = model
            fields = fields
            exclude = exclude

    data = json.loads(json_data)

    instance = model()
    for key, value in data.items():
        setattr(instance, key, value)

    serializer = CustomJSONSerializer
    deserialized = serializer.deserialize(json_data)

    assert instance.__dict__ == deserialized.__dict__

    serialized = serializer.serialize(instance)

    assert json.loads(serialized) == json.loads(json_data)

@pytest.mark.parametrize(
    "method_name, args",
    [
        ("serialize", [object()]),
        ("deserialize", '{"key":"value"}'),
    ],
)
def test_meta_validation_raises_when_missing(method_name, args):
    with pytest.raises(ValueError, match="Serializer class must define a Meta class with a 'model' attribute"):
        class CustomJSONSerializer(JSONSerializer):
            pass

        method = getattr(CustomJSONSerializer, method_name)
        method(*args)

@pytest.mark.parametrize(
    'model,fields,expectation',
    [
        (
            type('Person', (), {"name": str, "age": int}),
            ['name', 'age'],
            does_not_raise()
        ),
        (
            type('Student', (), {"id": int, "name": str, "room": int}),
            ['id', 'name', 'room', 'age'],
            pytest.raises(ValueError, match="Attribute 'age' does not exist on class 'Student'")
        ),
        (
            type('Room', (), {"id": int, "name": str}),
            ['id', 'room_name'],
            pytest.raises(ValueError, match="Attribute 'room_name' does not exist on class 'Room'")
        ),
    ]
)

def test_serializer_validates_meta_fields_on_method_call(model, fields, expectation):
    class CustomSerializer(JSONSerializer):
        class Meta(SerializerMeta):
            model = model
            fields = fields

    with expectation:
        CustomSerializer.serialize(model())
