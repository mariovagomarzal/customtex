"""This module contains the Text base class and its subclasses."""

import re

from customtex.configs import Config


# Parse text functions
def parse(text: str, config: Config) -> list[str]:
    """Parses the given text into a list of text or block tags (only top level)."""
    parsed_text = []

    beg_block, end_block = config.block_regex()
    block_mode = False

    current_text = ""
    for line in text.splitlines():
        if not block_mode:
            match_beg = re.fullmatch(beg_block, line)
            if match_beg:
                _, end_block = config.block_regex(match_beg.group(1))
                block_mode = True
                if current_text:
                    parsed_text.append(current_text)
                current_text = line + "\n"
            else:
                current_text += line + "\n"
        else:
            current_text += line + "\n"
            if re.fullmatch(end_block, line):
                block_mode = False
                parsed_text.append(current_text)
                current_text = ""

    if current_text:
        parsed_text.append(current_text)

    return parsed_text

def is_text(text: str, config: Config) -> bool:
    """Checks if the first line of the given text is different from the start block tag."""
    beg_block, _ = config.block_regex()
    return not re.fullmatch(beg_block, text.splitlines()[0])

# FIXME: Vars, multi and blocks could have the same names and that shouldn't be allowed
class Text():
    """Base class for text units without blocks in it.

    Attributes
    ----------
    text : str
        The text of the tag
    config : Config
        The config used to parse to find tags
    variables : list[str]
        A dictionary of variable names
    multi : dict[str, tuple[list[str], bool]]
        A dictionary of multioption names and their possible options

    Methods
    -------
    __init__(text: str, config: Config) -> None
        Initializes the text with the given text and config
        and parses the text to find variables and multioptions
    replace(options: dict[str, str]) -> str
        Returns the text with the given options replaced
    process(options: dict[str, str], defaults=False) -> str
        Returns the text with the given options replaced and
        asks the user for the missing options"""
    text: str
    config: Config
    variables: list[str]
    multi: dict[str, list[str]]

    def __init__(self, text: str, config: Config) -> None:
        self.text = text
        self.config = config

        # Get variables
        self.variables = []
        for name in re.findall(config.var_regex(), text):
            if name not in self.variables:
                self.variables.append(name)

        # Get multioptions
        self.multi = {}
        for match in re.findall(config.multi_regex(), text):
            name = match[0]
            if name not in self.multi:
                options = match[2]
                if options:
                    self.multi[name] = options.split(config.options_separator)
                else:
                    raise ValueError(f"Multioption '{name}' has no options in its first appearance")
                
    def replace(self, options: dict[str, str]) -> str:
        """Returns the text with the given options replaced."""
        text = self.text
        for name, value in options.items():
            text = re.sub(self.config.text_tag_regex(name), value, text)

        return text
    
    def process(self, options: dict[str, str]) -> str:
        """Returns the text with the given options replaced and the missing options asked to the user."""
        # Process variables
        for name in self.variables:
            if name not in options:
                print(f"Enter value for variable '{name}':")
                options[name] = input("Enter value: ")

        # Process multioptions
        for name, multi_options in self.multi.items():
            if name not in options:
                print(f"Select option for multioption '{name}':")
                for i, option in enumerate(multi_options):
                    print(f"{i+1}: {option}")
                options[name] = multi_options[int(input("Enter option: "))-1] # TODO: Check if valid option

        return self.replace(options)

class Block(Text):
    """Subclass of Text for text units that are blocks.

    Attributes
    ----------
    text : str
        The text of the tag
    config : Config
        The config used to parse to find tags
    name : str
        The name of the block
    blocks : dict[str, str]
        A dictionary of blocks and their content

    Methods
    -------
    __init__(text: str, config: Config) -> None
        Initializes the text with the given text and config
        and parses the text to find the different subblocks
    process(options: dict[str, str], defaults=False) -> str
        Returns the text of the block selected in the options or
        asked to the user if not given after being parsed and processed
        again with the given options"""
    name: str
    blocks: dict[str, str]

    def __init__(self, text: str, config: Config) -> None:
        self.text = text
        self.config = config

        text_lines = text.splitlines()
        beg_regex, _ = config.block_regex()
        beg_tag = re.fullmatch(beg_regex, text_lines[0])
        if beg_tag:
            self.name = beg_tag.group(1)
        else:
            raise ValueError(f"Block '{text_lines[0]}' is not a valid block")

        # Get blocks
        self.blocks = {}
        block_name = ""
        for line in text_lines[1:-2]:
            match = re.fullmatch(config.subblock_regex(self.name), line)
            if match:
                block_name = match.group(1)
                if block_name in self.blocks:
                    raise ValueError(f"Block '{block_name}' already exists")
                else:
                    self.blocks[block_name] = ""
            else:
                if block_name:
                    self.blocks[block_name] += line + "\n"
                else:
                    raise ValueError(f"Block '{line}' is not a valid block")

    def process(self, options: dict[str, str]) -> str:
        """Returns the block with the given options replaced and the missing options asked to the user."""
        if self.name not in options:
            blocks = list(self.blocks.keys())
            print(f"Choose block for '{self.name}':")
            for i, block_name in enumerate(blocks):
                print(f"  {i+1}. {block_name}")
            options[self.name] = blocks[int(input("Enter number: "))-1] # TODO: Check if input is valid

        parsed_block = parse(self.blocks[options[self.name]], self.config)
        final_output = ""
        for block in parsed_block:
            if is_text(block, self.config):
                final_output += Text(block, self.config).process(options)
            else:
                final_output += Block(block, self.config).process(options)

        return final_output
