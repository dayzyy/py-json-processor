from serializers.methods import json_serializer, xml_serializer

# Serialization related constants
JSON_INDENT = 2
XML_ROOT_ELEMENT_NAME = 'rooms'
XML_SHOW_ATTR_TYPE = False

SERIALIZERS = {
    "json": lambda data: json_serializer(data, indent=JSON_INDENT),
    "xml": lambda data: xml_serializer(data, custom_root=XML_ROOT_ELEMENT_NAME, attr_type=XML_SHOW_ATTR_TYPE)
}
