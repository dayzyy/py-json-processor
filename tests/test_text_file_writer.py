import pytest
from file_handlers.base_file_writers import TextFileWriter

@pytest.mark.parametrize(
    'content',
    [
        '{"name": "Luka", "age": 20}',  # JSON content
        '<room><name>Room 101</name><id>1</id></room>',  # XML content
        'name,age\nLuka,20\n'  # CSV content
    ]
)
def test_text_file_writer_writes_content_correctly(tmp_path, content):
    TextFileWriter.write(tmp_path, content)

    with open(tmp_path, 'r', encoding='utf-8') as f:
        read_content = f.read()

    assert read_content == content

def test_text_file_writer_overwrites_existing_file(tmp_path):
    initial_content = "Old content"
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(initial_content)

    new_content = "New content"
    TextFileWriter.write(tmp_path, new_content)

    with open(tmp_path, 'r', encoding='utf-8') as f:
        read_content = f.read()

    assert read_content == new_content

def test_text_file_writer_file_not_found():
    with pytest.raises(FileNotFoundError):
        TextFileWriter.write('/invalid/path/to/file.txt', 'content')
