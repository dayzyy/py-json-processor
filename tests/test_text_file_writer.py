import pytest
import tempfile
import os
from file_handlers.base_file_writers import TextFileWriter

# Create a temporary file and provide path to it
@pytest.fixture
def tmp_path():
    with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp:
        tmp_path = tmp.name

    yield tmp_path
    os.remove(tmp.name)

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
