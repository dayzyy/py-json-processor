import pytest
from file_handlers.base_file_readers import TextFileReader

@pytest.mark.parametrize(
    'content',
    [
        '{"name": "Luka", "age": 20}',  # JSON content
        '<room><name>Room 101</name><id>1</id></room>',  # XML content
        'name,age\nLuka,20\n'  # CSV content
    ]
)
def test_text_file_reader_reads_content_correctly(tmp_path, content):
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(content)

    result = TextFileReader.read(tmp_path)
    assert result == content

def test_text_file_reader_file_not_found():
    with pytest.raises(FileNotFoundError):
        TextFileReader.read('non_existent_file.txt')
