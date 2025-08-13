from cli.parse_arguments import parse_arguments
from file_handlers.base_file_readers import TextFileReader
from file_handlers.base_file_writers import TextFileWriter
from serializers.custom_serializers import StudentJSONSerializer, RoomJSONSerializer
from app.combine import combine
from exporters.factory import ExporterFactory


# Core business logic
def run(students_file: str, rooms_file: str, output_format: str, output_file: str):
    students_data = TextFileReader.read(students_file)
    rooms_data = TextFileReader.read(rooms_file)

    students = StudentJSONSerializer.deserialize_list(students_data)
    rooms = RoomJSONSerializer.deserialize_list(rooms_data)

    combined = combine(students, rooms)

    exporter = ExporterFactory.get_exporter(output_format)
    formatted_data = exporter(combined)

    TextFileWriter.write(output_file, formatted_data)


def main():
    args = parse_arguments()
    run(
        students_file=args.students_file,
        rooms_file=args.rooms_file,
        output_format=args.output_format,
        output_file=args.output_file
    )

if __name__ == "__main__":
    main()
