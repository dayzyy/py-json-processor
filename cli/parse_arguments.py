import argparse
from settings import SERIALIZERS

AVAILABE_FORMATS = [format for format in SERIALIZERS.keys()]

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Combine students and rooms data into a single output file."
    )

    parser.add_argument(
        "-sf",
        "--students-file",
        required=True,
        help="Path to the students JSON file."
    )
    parser.add_argument(
        "-rf",
        "--rooms-file",
        required=True,
        help="Path to the rooms JSON file."
    )
    parser.add_argument(
        "-of",
        "--output-format",
        required=True,
        choices=AVAILABE_FORMATS,
        help=f"Output format. Must be one of the listed {AVAILABE_FORMATS}."
    )
    parser.add_argument(
        "-fmt",
        "--output-file",
        required=True,
        help="Path to save the generated output file."
    )

    return parser.parse_args()
