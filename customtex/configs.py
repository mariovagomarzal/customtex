"""This module contains the Config class that stores the configuration of a template."""

from pathlib import Path
import json


# Default configs paths
TEMPLATES_CONFIGS_PATH = Path(__file__).parent / "templates_configs"
DEFAULT_CONFIG_PATH = TEMPLATES_CONFIGS_PATH / "default_config.json"
EMPTY_CONGIF_PATH = TEMPLATES_CONFIGS_PATH / "empty_config.json"

# Regex constants
KEY_WORDS_TEXT = r"(var|multi)"
TAG_NAME = r"[a-zA-Z_]\w*"


class Config():
    """Stores the configuration of a template.
    This includes the start and the end characters of a tag
    and the seperator character of options.

    Attributes
    ----------
    start_tag : str
        The start character of a tag
    end_tag : str
        The end character of a tag
    options_separator : str
        The character that separates options in a tag

    Methods
    -------
    var_regex() -> str
        Returns a regex string that matches a variable tag
    multi_regex() -> str
        Returns a regex string that matches a multioption tag
    block_regex() -> tuple[str, str]
        Returns a tuple of regex strings that match the start and end of a block tag
    subblock_regex(block_name: str) -> str
        Returns a regex string that matches a subblock tag of the given block name
    """

    def __init__(self, path=DEFAULT_CONFIG_PATH) -> None:
        """Reads the config file of the given path and stores the config.

        Exceptions:
            FileNotFoundError: If the file does not exist
            json.JSONDecodeError: If the file is not a valid json file
            KeyError: If the file does not contain all the required keys
            ValueError: If some special characters are empty
        """
        with open(path, "r") as file:
            config = json.load(file)

        self.start_tag = config["start_tag"]
        self.end_tag = config["end_tag"]
        self.options_separator = config["options_separator"]

        # Check that special characters are not empty
        if not self.start_tag:
            raise ValueError("Config start tag cannot be empty")
        if not self.end_tag:
            raise ValueError("Config end tag cannot be empty")
        if not self.options_separator:
            raise ValueError("Config options separator cannot be empty")

    def __repr__(self) -> str:
        return f"Config(start_tag={self.start_tag!r}, end_tag={self.end_tag!r}, \
options_separator={self.options_separator!r})"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def text_tag_regex(self, name: str) -> str:
        """Returns a regex string that matches a text tag with the given name."""
        return self.start_tag + KEY_WORDS_TEXT + r":(" + name + r")" + self.end_tag
    
    def var_regex(self, name=TAG_NAME) -> str:
        """Returns a regex string that matches a variable tag."""
        return self.start_tag + r"var:(" + name + r")" + self.end_tag
    
    def multi_regex(self, name=TAG_NAME) -> str:
        """Returns a regex string that matches a multioption tag."""
        return self.start_tag + r"multi:(" + name + r")(=(.*?(\|.*?)+?)){0,1}" + self.end_tag
    
    def block_regex(self, name=TAG_NAME) -> tuple[str, str]:
        """Returns a tuple of regex strings that match the start and end of a block tag."""
        return self.start_tag + r"block:(" + name + r")" + self.end_tag, \
               self.start_tag + r"endblock:(" + name + r")" + self.end_tag
    
    def subblock_regex(self, block_name: str, option_name=TAG_NAME) -> str:
        """Returns a regex string that matches a subblock tag of the given block name."""
        return self.start_tag + block_name + r":(" + option_name + r")" + self.end_tag
