import pytest
from file_handlers.base_file_readers import TextFileReader
import tempfile
import os

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
        '<room><name>Room 101</name><id>1</id></room>'  # XML content
    ]
)
def test_text_file_reader_reads_content_correctly(tmp_path, content):
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(content)

    result = TextFileReader.read(tmp_path)
    assert result == content
