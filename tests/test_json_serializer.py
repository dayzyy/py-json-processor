from typing import List, Optional
import pytest
from serializers.base_serializers import BaseSerializer, SerializerMeta, JSONSerializer
import json
from contextlib import nullcontext as does_not_raise
from models.base_models import Model

@pytest.mark.parametrize(
    'model,fields,exclude,json_data',
    [
        (
            type('Person', (Model,), {"__annotations__": {'name': str, 'age': int}}),
            None, None,
            '{"name": "Luka", "age": 20}'
        ),
        (
            type('Student', (Model,), {"__annotations__": {'id': int, 'name': str, 'room': int}}),
            None, None,
            '{"id": 0, "name": "Luka", "room": 111}'
        ),
        (
            type('Room', (Model,), {"__annotations__": {'id': int, 'name': str}}),
            None, None,
            '{"id": 19, "name": "Room #19"}'
        )
    ]
)
def test_json_serializer_serialize_and_deserialize_methods(model, fields: Optional[List[str]], exclude: Optional[List[str]], json_data: str):
    class Meta(SerializerMeta):
        pass

    Meta.model = model
    Meta.fields = fields
    Meta.exclude = exclude

    class CustomJSONSerializer(JSONSerializer):
        pass

    CustomJSONSerializer.Meta = Meta

    data = json.loads(json_data)

    instance = model(**data)

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
    'model,instance_kwargs,fields,expectation',
    [
        (
            type('Person', (Model,), {"__annotations__": {"name": str, "age": int}}),
            {"name": "Luka", "age": 20},
            ['name', 'age'],
            does_not_raise()
        ),
        (
            type('Student', (Model,), {"__annotations__": {"id": int, "name": str, "room": int}}),
            {"id": 0, "name": "Luka", "room": 111},
            ['id', 'name', 'room', 'age'],
            pytest.raises(ValueError, match="Attribute 'age' does not exist on class 'Student'")
        ),
        (
            type('Room', (Model,), {"__annotations__": {"id": int, "name": str}}),
            {"id": 111, "name": "Room #111"},
            ['id', 'room_name'],
            pytest.raises(ValueError, match="Attribute 'room_name' does not exist on class 'Room'")
        ),
    ]
)
def test_serializer_validates_meta_fields_on_method_call(model, instance_kwargs, fields, expectation):
    class Meta(SerializerMeta):
        pass

    Meta.model = model
    Meta.fields = fields

    class CustomSerializer(JSONSerializer):
        pass

    CustomSerializer.Meta = Meta

    with expectation:
        CustomSerializer.serialize(model(**instance_kwargs))

@pytest.mark.parametrize(
    'model, json_list_str, expected_instances',
    [
        (
            type('Person', (Model,), {"__annotations__": {'name': str, 'age': int}}),
            '[{"name": "Luka", "age": 20}, {"name": "Anna", "age": 25}]',
            [
                type('Person', (Model,), {"__annotations__": {'name': str, 'age': int}})(name="Luka", age=20),
                type('Person', (Model,), {"__annotations__": {'name': str, 'age': int}})(name="Anna", age=25),
            ]
        ),
        (
            type('Student', (Model,), {"__annotations__": {'id': int, 'name': str, 'room': int}}),
            '[{"id": 0, "name": "Luka", "room": 111}, {"id": 1, "name": "Anna", "room": 222}]',
            [
                type('Student', (Model,), {"__annotations__": {'id': int, 'name': str, 'room': int}})(id=0, name="Luka", room=111),
                type('Student', (Model,), {"__annotations__": {'id': int, 'name': str, 'room': int}})(id=1, name="Anna", room=222),
            ]
        ),
    ]
)
def test_json_serializer_deserialize_lists_method(model, json_list_str, expected_instances):
    class Meta(SerializerMeta):
        pass

    Meta.model = model

    class CustomJSONSerializer(JSONSerializer):
        pass

    CustomJSONSerializer.Meta = Meta

    instances = CustomJSONSerializer.deserialize_list(json_list_str)

    assert len(instances) == len(expected_instances)
    for actual, expected in zip(instances, expected_instances):
        assert actual.__dict__ == expected.__dict__
