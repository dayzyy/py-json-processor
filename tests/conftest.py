import pytest
import tempfile
import os

# Create a temporary file and provide path to it
@pytest.fixture
def tmp_path():
    with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp:
        tmp_path = tmp.name

    yield tmp_path
    os.remove(tmp.name)
