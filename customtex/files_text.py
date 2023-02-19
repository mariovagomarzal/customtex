from pathlib import Path
from customtex.load_presets import *


# Constants for the text files
TAB = "  "

def main_text(args):
    # Document class
    main = f"\\documentclass[{args.documentoptions}]{{{args.documentclass}}}\n\n"
    
    # Input preamble and macros
    main += "\\input{tex/preamble.tex}\n"
    main += "\\input{tex/macros.tex}\n\n"

    # Title
    if args.includetitle:
        main += f"\\title{{{args.title}}}\n"
        main += f"\\author{{{args.author}}}\n"
        main += f"\\date{{{args.date}}}\n\n"

    # Document content
    main += "\\begin{document}\n"
    main += TAB + ("\\maketitle\n" + TAB if args.includetitle else "") + "\n"
    main += "\\end{document}\n"

    return main

def preamble_text(args):
    preamble = []

    # Language
    preamble.append(f"\\usepackage[{args.language}]{{babel}}\n")

    # Title
    if args.titlestyle:
        title_style = get_style("title", args.titlestyle, args.documentclass)
        preamble.append("\\usepackage{titling}\n\n" + title_style)
    
    # Margins
    if args.custommargins:
        preamble.append(f"\\usepackage[{args.custommargins}]{{geometry}}\n")
    else:
        if args.margins == "normal":
            preamble.append("\\usepackage[margin=2.54cm]{geometry}\n")
        elif args.margins == "wide":
            preamble.append("\\usepackage[margin=3.17cm]{geometry}\n")

    # 'xcolor' package
    if args.xcolor:
        if args.xcoloroptions:
            preamble.append(f"\\usepackage[{args.xcoloroptions}]{{xcolor}}\n")
        else:
            preamble.append("\\usepackage{xcolor}\n")

    # Section style
    if args.sectionstyle:
        section_style = get_style("section", args.sectionstyle, args.documentclass)
        preamble.append("\\usepackage{titlesec}\n\n" + section_style)

    # 'hyperref' package
    if args.hyperref:
        hypersetup = ""
        if args.hypersetup:
            hypersetup = get_hypersetup(args.hypersetup) + "\n"
        preamble.append("\\usepackage{hyperref}\n" + hypersetup)
    
    # 'graphicx' package
    if args.graphicx:
        graphicxpath = ""
        if args.graphicxpath:
            graphicxpath = f"\\graphicspath{{ {{{args.graphicxpath}}} }}\n"
            (Path(args.path) / Path(args.graphicxpath)).mkdir(exist_ok=True)
        preamble.append("\\usepackage{graphicx}\n" + graphicxpath)

    # 'mathtools' package
    if args.mathtools:
        preamble.append("\\usepackage{mathtools}\n")

    # Theorem styles
    if args.theoremstyle:
        theoremstyle = get_theoremstyle(args.theoremstyle, args.theoremsparent, args.language)
        preamble.append("\\usepackage{amsthm}\n\\usepackage{thmtools}\n\n" + theoremstyle)

    return "\n".join(preamble)


def macros_text(args):
    if args.macros:
        return get_macros(args.macros) + "\n"
    else:
        return ""
