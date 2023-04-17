import regex as re


def parse(text: str) -> list[str]:
    return [] # TODO: Parse text into parts, were each part is either text (with variables and multi), switch or include (top level only)

def is_text(text: str) -> bool:
    return True # TODO: Check if text is text (with variables and multi), switch or include (top level only)

class Part():
    text: str

    def __init__(self, text: str) -> None:
        self.text = text

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.text!r})"
    
    def process(self, defaults=False) -> str:
        return self.text

class Text(Part):
    variables: dict[str, str]
    multi: dict[str, tuple[list[str], bool]]

    def __init__(self, text: str) -> None:
        self.text = text

        # Get variables: <var:varname> or <var:varname=default>
        self.variables = {}
        for match in re.findall(r"<var:(.+?)(=.*?){0,1}>", text):
            name, default = match
            if name in self.variables:
                if self.variables[name] and default:
                    raise ValueError(f"Variable '{name}' already has a default value")
            else:
                self.variables[name] = default[1:] if default else ""

        # Get multioptions: <multi:varname=option1|...|optionN> or <multi:varname==option1|...|optionN>
        self.multi = {}
        for match in re.findall(r"<multi:([^=]+?)(=(=){0,1}((.*?)\|(.*?\|)*?(.*?))){0,1}>", text):
            name, _, default, options, _, _, _ = match
            if name in self.multi:
                if options:
                    raise ValueError(f"Multioption '{name}' already has options")
            else:
                if options:
                    self.multi[name] = (options.split("|"), default == "=")
                else:
                    raise ValueError(f"Multioption '{name}' has no options")
                
    def replace(self, options: dict[str, str]) -> str:
        text = self.text
        for name, value in options.items():
            pass # TODO: Replace variables and multioptions with values

        return text
    
    def process(self, defaults=False) -> str:
        # Get variable options
        options = {}
        for name, default in self.variables.items():
            if defaults and default:
                options[name] = default
            else:
                options[name] = input(f"Enter value for variable '{name}': ")

        # Get multioptions options
        for name, (multioptions, default) in self.multi.items():
            if defaults and default:
                options[name] = multioptions[0]
            else:
                print(f"Choose option for multioption '{name}':")
                for i, option in enumerate(multioptions):
                    print(f"  {i+1}. {option}")
                options[name] = multioptions[int(input("Enter number: "))-1]

        return self.replace(options)

class Switch(Part):
    blocks: dict[str, str]

    def __init__(self, text: str) -> None:
        self.text = text

        # TODO: See if it is a switch or an include

    def process(self, defaults=False) -> str:
        # TODO: Use defaults
        text = ""

        print("Choose block to use:")
        for i, name in enumerate(self.blocks.keys()):
            print(f"  {i+1}. {name}")
        block = self.blocks[list(self.blocks.keys())[int(input("Enter number: "))-1]]

        parsed_block = parse(block)
        for part in parsed_block:
            if is_text(part):
                text += Text(part).process()
            else:
                text += Switch(part).process()

        return text

class File():
    name: str
    parts: list[Part]

    def __init__(self, name: str, text: str) -> None:
        self.name = name

        parsed_text = parse(text)

        self.parts = []
        for part in parsed_text:
            if is_text(part):
                self.parts.append(Text(part))
            else:
                self.parts.append(Switch(part))

    def process(self, defaults=False) -> str:
        text = ""

        for part in self.parts:
            text += part.process(defaults)

        return text
