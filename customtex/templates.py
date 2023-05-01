"""This module contains the File and the Template classes."""

import re
from pathlib import Path

from customtex.defaults import *
from customtex.configs import Config
from customtex.texts import parse, is_text, Text, Block


def parse_template(text: str, config: Config) -> dict[str, str]:
    return {}


class File():
    name: str
    config: Config
    content: list[Text]

    def __init__(self, name: str, config: Config, text: str) -> None:
        self.name = name
        self.config = config

        for unit in parse(text, config):
            if is_text(unit, config):
                self.content.append(Text(unit, config))
            else:
                self.content.append(Block(unit, config))

    def get_path(self, parent_path: Path) -> Path:
        return parent_path / self.name

    def process(self, options: dict[str, str]) -> str:
        processed_text = ""
        for unit in self.content:
            processed_text += unit.process(options)

        return processed_text
    
    def write_file(self, parent_path: Path, options: dict[str, str], overwrite: bool = False) -> None:
        processed_text = self.process(options)
        path = self.get_path(parent_path)

        if overwrite:
            with open(path, "w") as file:
                file.write(processed_text)
        else:
            with open(path, "x") as file:
                file.write(processed_text)

class Template():
    name: str
    config: Config
    files: list[File]

    def __init__(self, dir_path: Path):
        self.name = dir_path.name
        try:
            self.config = Config(dir_path / "config.json")
        except FileNotFoundError:
            self.config = Config()

        # Find all the files with the TEMPLATE_EXTENSION extension and parse them
        self.files = []
        for file_path in dir_path.glob(f"*{TEMPLATE_EXTENSION}"):
            with open(file_path) as file:
                parsed_template = parse_template(file.read(), self.config)
                for name, text in parsed_template.items():
                    self.files.append(File(name, self.config, text))

    def write_files(self, path: Path, options: dict[str, str], overwrite=False) -> None:
        for file in self.files:
            file.write_file(path, options, overwrite)
