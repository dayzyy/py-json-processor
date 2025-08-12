import json
from typing import Any
import dicttoxml

def json_serializer(data: Any, indent: int = 2 ) -> str:
    return json.dumps(data, indent=indent)

def xml_serializer(data: Any, *, custom_root: str = 'root', attr_type: bool = True) -> str:
    xml_bytes = dicttoxml.dicttoxml(data, custom_root=custom_root, attr_type=attr_type)
    return xml_bytes.decode() if isinstance(xml_bytes, bytes) else xml_bytes
