from customtex import *
from pathlib import Path
import sys
from stringcolor import *


# Output messages
def info_message(message):
    return cs("(i)", "yellow").bold() + cs(f" {message}", "white")

def success_message(message):
    return cs("(\u2713)", "green").bold() + cs(f" {message}", "white")


# 'customtex' command
def customtex():
    args = parse_args(sys.argv[1:])
    path = Path(args.path)
    
    colored_path = cs(path.absolute(), "blue").underline()
    print(info_message(f"Initializing project at '{colored_path}'..."))

    (path / "tex").mkdir(exist_ok=True)

    with open(path / f"{args.name}.tex", "w") as main:
        main.write(main_text(args))

    with open(path / "tex" / "preamble.tex", "w") as preamble:
        preamble.write(preamble_text(args))

    with open(path / "tex" / "macros.tex", "w") as macros:
        macros.write(macros_text(args))

    print(success_message("Project initialized successfully!"))

    return 0
