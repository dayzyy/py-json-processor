from cli.parse_arguments import parse_arguments
from file_handlers.base_file_readers import TextFileReader
from file_handlers.base_file_writers import TextFileWriter
from serializers.custom_serializers import StudentJSONSerializer, RoomJSONSerializer

def main():
    args = parse_arguments()

    students_data = TextFileReader.read(args.student_file)
    rooms_data = TextFileReader.read(args.rooms_file)

if __name__ == "__main__":
    main()
