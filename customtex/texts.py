"""This module contains the Text base class and its subclasses."""
import re

from customtex.configs import Config


# Parse text functions
def parse(text: str, config: Config) -> list[str]:
    """Parses the given text into a list of text or block tags (only top level).)"""
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

class Text():
    text: str
    config: Config
    variables: dict[str, tuple[str, bool]]
    multi: dict[str, tuple[list[str], bool]]

    def __init__(self, text: str, config: Config) -> None:
        self.text = text
        self.config = config

        # Get variables
        self.variables = {}
        for match in re.findall(config.var_regex(), text):
            name, is_default, default = match[0], match[1], match[3]
            if name in self.variables:
                if is_default:
                    raise ValueError(f"Variable '{name}' already has a default value")
            else:
                self.variables[name] = (default, bool(is_default))

        # Get multioptions
        self.multi = {}
        for match in re.findall(config.multi_regex(), text):
            name, is_definition, is_default, options = match[0], match[2], match[3], match[4]
            if name in self.variables:
                raise ValueError(f"Multioption '{name}' already exists as a variable")
            elif name in self.multi:
                if is_default:
                    raise ValueError(f"Multioption '{name}' already has a default value")
            elif is_definition:
                self.multi[name] = (options.split(config.options_separator), bool(is_default))
            else:
                raise ValueError(f"Multioption '{name}' is not defined")

                
    def replace(self, options: dict[str, str]) -> str:
        """Returns the text with the given options replaced."""
        text = self.text
        for name, value in options.items():
            text = re.sub(self.config.text_tag_regex(name), value, text)

        return text
    
    def process(self, options: dict[str, str], defaults=False) -> str:
        """Returns the text with the given options replaced and the missing options asked to the user.
        If defaults is True, the default values will be used instead of asking the user."""
        # Process variables
        for name, (default, has_default) in self.variables.items():
            if name not in options:
                if has_default and defaults:
                    options[name] = default
                else:
                    options[name] = input(f"Enter value for variable '{name}': ")

        # Process multioptions
        for name, (options_list, has_default) in self.multi.items():
            if name not in options:
                if has_default and defaults:
                    options[name] = options_list[0]
                else:
                    print(f"Choose option for multioption '{name}':")
                    for i, option in enumerate(options_list):
                        print(f"  {i+1}. {option}")
                    # TODO: Check if input is valid
                    options[name] = options_list[int(input("Enter number: "))-1]

        return self.replace(options)

class Block(Text): # FIXME: Use default values for blocks
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

    def process(self, options: dict[str, str], defaults=False) -> str:
        """Returns the block with the given options replaced and the missing options asked to the user.
        If defaults is True, the default values will be used instead of asking the user."""
        if self.name not in options:
            blocks = list(self.blocks.keys())
            print(f"Choose block for '{self.name}':")
            for i, block_name in enumerate(blocks):
                print(f"  {i+1}. {block_name}")
            # TODO: Check if input is valid
            options[self.name] = blocks[int(input("Enter number: "))-1]

        parsed_block = parse(self.blocks[options[self.name]], self.config)
        final_output = ""
        for block in parsed_block:
            if is_text(block, self.config):
                final_output += Text(block, self.config).process(options, defaults)
            else:
                final_output += Block(block, self.config).process(options, defaults)

        return final_output

class File():
    name: str
    parts: list[Text]

class Template():
    pass
