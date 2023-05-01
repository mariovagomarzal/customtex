import pytest
from pathlib import Path

from customtex import *


# Helper functions
CURRENT_DIR = Path(__file__).parent

def load_text_file(file_name: str) -> str:
    """Loads the text file with the given name and returns its content."""
    with open(CURRENT_DIR / file_name) as file:
        return file.read()


# Tests for 'parse' function
def test_parse():
    with open(CURRENT_DIR / "parse.txt") as file:
        text = file.read()

    # TODO: Test
    pass

# Tests for 'is_text' function
def test_is_text():
    pass

# Tests for 'Text' class
def test_text_init():
    texts: list[str] = []
    for i in range(1):
        texts.append(load_text_file(f"text{i + 1}.txt"))
    config = Config()

    # Test text 1
    text = Text(texts[0], config)
    assert text.variables == {
        "name1": ("default1", True),
        "name2": ("", False),
        "name3": ("default 3", True),
        "name4": ("", True),
    }
    assert text.multi == {
        "name5": (["option1", "option2"], False),
        "name6": (["option1", "option 2", "option 3"], True)
    }

    # Test text 2
    # text = Text(texts[1], config)
    
