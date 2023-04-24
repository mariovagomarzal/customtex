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

class Block(Text):
    blocks: dict[str, str]

    def __init__(self, text: str, config: Config) -> None:
        self.text = text
        self.config = config

        # Get blocks:

    def process(self, options: dict[str, str], defaults=False) -> str:
        # TODO: Use defaults
        text = ""

        print("Choose block to use:")
        for i, name in enumerate(self.blocks.keys()):
            print(f"  {i+1}. {name}")
        block = self.blocks[list(self.blocks.keys())[int(input("Enter number: "))-1]]

        parsed_block = parse(block, self.config)
        for part in parsed_block:
            if is_text(part, self.config):
                text += Text(part, self.config).process(options)
            else:
                text += Block(part, self.config).process(options)

        return text

class File():
    name: str
    parts: list[Text]

class Template():
    pass
