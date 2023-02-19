import json
from pathlib import Path


# Constants
PRESETS_PATH = Path(__file__).parent / "presets"

# Choices functions
def get_choices(option):
    with open(PRESETS_PATH / f"{option}.json", "r") as file:
        return list(json.load(file).keys())

# Language
def get_language(language):
    with open(PRESETS_PATH / "languages.json", "r") as file:
        return json.load(file)[language]

# Title and section styles
def load_style(item, style_name):
    with open(PRESETS_PATH / f"{item}styles.json", "r") as file:
        return json.load(file)[style_name]
    
def split_dclasses(style):
    for key in list(style.keys()):
        splitted_key = key.replace(" ", "").split(",")
        if len(splitted_key) > 1:
            for word in splitted_key:
                style[word] = style[key]

            del style[key]

def get_style_dclasses(style):
    dclasses = list(style.keys())
    dclasses.remove("default")
    return dclasses

def get_style(item, style_name, dclass):
    style = load_style(item, style_name)
    split_dclasses(style)
    if dclass not in get_style_dclasses(style):
        dclass = style["default"]
    
    return "\n".join(style[dclass])

# Hyperref setups
def load_hypersetup(setup_name):
    with open(PRESETS_PATH / "hypersetups.json", "r") as file:
        return json.load(file)[setup_name]
    
def get_hypersetup(setup_name):
    hypersetup = load_hypersetup(setup_name)
    output = "\\hypersetup{\n"
    output += "\n".join(hypersetup) + "\n}"
    return output

# Theorem styles
def load_theoremstyle(style_name):
    with open(PRESETS_PATH / "theoremstyles.json", "r") as file:
        return json.load(file)[style_name]
    
def get_theoremstyle(style_name, theoremsparent, language):
    theorems_style = load_theoremstyle(style_name)
    language = get_language(language)["mathnames"]

    output = ""
    if theorems_style["styles"]:
        output += "\n".join(theorems_style["styles"]) + "\n\n"
    
    for theorem in list(theorems_style["enviorments"].keys()):
        theorem_style = theorems_style["enviorments"][theorem]
        theorem_name = language[theorem]
        if theorem_style:
            output += f"\\declaretheorem[name={theorem_name}, style={theorem_style}, numberwithin={theoremsparent}]{{{theorem}}}\n"
            output += f"\\declaretheorem[name={theorem_name}, style={theorem_style}, numbered=no]{{{theorem}*}}\n"
        else:
            output += f"\\declaretheorem[name={theorem_name}, numberwithin={theoremsparent}]{{{theorem}}}\n"
            output += f"\\declaretheorem[name={theorem_name}, numbered=no]{{{theorem}*}}\n"

    return output[:-1]

# Macros
def load_macros():
    with open(PRESETS_PATH / "macros.json", "r") as file:
        return json.load(file)

def get_macros(macros_names):
    macros = load_macros()
    return "\n\n".join(["\n".join(macros[name]) for name in macros_names])

# Templates
def load_templates():
    with open(PRESETS_PATH / "templates.json", "r") as file:
        return json.load(file)

def get_template(template_name):
    templates = load_templates()
    return templates[template_name]
