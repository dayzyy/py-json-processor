# Serializers

This directory contains the base and custom serializers used to convert model instances to and from various formats (e.g., JSON, XML).

## Overview

A serializer defines how to transform a model instance into a specific format (serialization) and how to reconstruct a model instance from that format (deserialization).

## Base and Concrete serializers

**Base serializers** (e.g., JSONSerializer, XMLSerializer) are responsible for implementing the actual serialize() and deserialize() methods for a given data format.
They do not know anything about a specific model — only how to handle the format.

**Concrete serializers** are subclasses of a base serializer that define a Meta class to tell the serializer which model to work with and which fields to include or exclude.
They do not define the format logic themselves — they just configure the base serializer for a specific model.

### Examples:
```python
# Base serializer for JSON format (knows how to handle JSON)
class JSONSerializer(BaseSerializer):
    @classmethod
    @BaseSerializer.ensure_meta
    def serialize(cls, instance, *args, indent=2, **kwargs):
        fields = cls._get_fields()
        data = {field: getattr(instance, field) for field in fields}
        return json.dumps(data, indent=indent)

    @classmethod
    @BaseSerializer.ensure_meta
    def deserialize(cls, data, *args, **kwargs):
        model = cls._get_meta().model
        return model(**json.loads(data))


# Concrete serializer for Student model using JSON
class StudentJSONSerializer(JSONSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "room"]
```

## Extending BaseSerializer to create a serializer for a new data format

To add support for a new format:

    1.Subclass BaseSerializer.
    2.Implement both serialize() and deserialize() methods.
    3.Wrap both methods with the @BaseSerializer.ensure_meta decorator to ensure that the Meta class is defined before the method runs.
    4.Use _get_fields() to retrieve the list of fields to serialize.
    5.Use _get_meta() to retrieve the Meta configuration (e.g., model class).

### Examples:
```python
class YAMLSerializer(BaseSerializer):
    @classmethod
    @BaseSerializer.ensure_meta
    def serialize(cls, instance, *args, **kwargs):
        import yaml
        fields = cls._get_fields()
        data = {field: getattr(instance, field) for field in fields}
        return yaml.dump(data)

    @classmethod
    @BaseSerializer.ensure_meta
    def deserialize(cls, data, *args, **kwargs):
        import yaml
        model = cls._get_meta().model
        parsed_data = yaml.safe_load(data)
        return model(**parsed_data)
```

## The Meta class

Each serializer must define a Meta class containing following class attributes:

    - model: The model class this serializer works with. (Required)
    - fields: Optional list of field names to include. If omitted, all model fields are used.
    - exclude:	Optional list of field names to exclude. Cannot be used together with fields.

### Examples:
```python
class StudentJSONSerializer(JSONSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "room"]

class RoomJSONSerializer(JSONSerializer):
    class Meta:
        model = Room
        exclude = ["private_notes"]
```
