from cli.parse_arguments import parse_arguments
from file_handlers.base_file_readers import TextFileReader
from file_handlers.base_file_writers import TextFileWriter
from serializers.custom_serializers import StudentJSONSerializer, RoomJSONSerializer
from app.combine import combine
import json
import dicttoxml

def main():
    args = parse_arguments()

    students_data = TextFileReader.read(args.students_file)
    rooms_data = TextFileReader.read(args.rooms_file)

    students = StudentJSONSerializer.deserialize_list(students_data)
    rooms = RoomJSONSerializer.deserialize_list(rooms_data)

    combined = combine(students, rooms)

    if args.output_format == 'json':
        formated_data = json.dumps(combined)
    else:
        xml_data = dicttoxml.dicttoxml(combined, custom_root='rooms', attr_type=False)

        if isinstance(xml_data, bytes):
            formated_data = xml_data.decode()
        else:
            formated_data = xml_data

    TextFileWriter.write(args.output_file, formated_data)

if __name__ == "__main__":
    main()
