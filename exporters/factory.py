from typing import Callable
from exporters.formats import ExporterFormats
from exporters.exporters import json_exporter, xml_exporter
from settings import JSON_INDENT, XML_ROOT_ELEMENT_NAME, XML_SHOW_ATTR_TYPE

class ExporterFactory:
    EXPORTERS: dict[ExporterFormats, Callable] = {
        ExporterFormats.JSON: lambda data: json_exporter(data, indent=JSON_INDENT),
        ExporterFormats.XML: lambda data: xml_exporter(data, custom_root=XML_ROOT_ELEMENT_NAME, attr_type=XML_SHOW_ATTR_TYPE)
    }

    @classmethod
    def get_exporter(cls, format: str):
        try:
            enum_format = ExporterFormats(format)
            return cls.EXPORTERS[enum_format]
        except KeyError:
            raise ValueError(f"Unsupported export format: {format}")
