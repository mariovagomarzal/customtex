import argparse
from importlib.metadata import version
from customtex.load_presets import get_choices, get_template


def get_parser():
    parser = argparse.ArgumentParser(prog="customtex", description="CustomTeX - A LaTeX wrapper for customizing documents")

    parser.add_argument("-v", "--version", action="version", version=f"customtex {version('customtex')}", help="Show the version of CustomTeX and exit")

    parser.add_argument("-p", "--path", default=".", help="Path to the project directory")
    parser.add_argument("-n", "--name", default="main", help="Name of the main file (whose extension is always '.tex')")
    parser.add_argument("-l", "--language", choices=get_choices("languages"), default="english", help="Language to use for the document")

    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # "init" subcommand
    init_parser = subparsers.add_parser("init", help="Initialize a new project")

    # Document class
    documentclass_group = init_parser.add_argument_group(title="documentclass options")
    documentclass_group.add_argument("--documentclass", default="article", help="Document class to use for the project")
    documentclass_group.add_argument("--documentoptions", default="a4paper, 11pt", help="Document options to use for the project")

    # Title
    title_group = init_parser.add_argument_group(title="title options")
    title_group.add_argument("--includetitle", action="store_true", help="Include the title")
    title_group.add_argument("--title", default="", help="Title to use for the document")
    title_group.add_argument("--author", default="", help="Author to use for the document")
    title_group.add_argument("--date", default="", help="Date to use for the document")
    title_group.add_argument("--titlestyle", choices=get_choices("titlestyles"), help="Title style to use for the document")

    # Miscelaneous
    misc_group = init_parser.add_argument_group(title="miscelaneous options")

    # Margins
    margins_group = misc_group.add_mutually_exclusive_group()
    margins_group.add_argument("--margins", choices=["normal", "wide"], default="normal", help="Margins to use for the document")
    margins_group.add_argument("--custommargins", help="Custom margins to use for the document")

    # Package "xcolor"
    misc_group.add_argument("--xcolor", action="store_true", help="Include 'xcolor' package")
    misc_group.add_argument("--xcoloroptions", help="Options to use for the package 'xcolor'")

    # Sections and headers
    misc_group.add_argument("--sectionstyle", choices=get_choices("sectionstyles"), help="Section style to use for the document") 
    misc_group.add_argument("--headerstyle", choices=get_choices("headerstyles"), help="Header style to use for the document")

    # Package "hyperref"
    misc_group.add_argument("--hyperref", action="store_true", help="Include 'hyperref' package")
    misc_group.add_argument("--hypersetup", choices=get_choices("hypersetups"), help="Hyperref setup to use for the document")

    # Package "graphicx"
    misc_group.add_argument("--graphicx", action="store_true", help="Include 'graphicx' package")
    misc_group.add_argument("--graphicxpath", help="Name of the directory where the figures are stored")

    # Mathemathics
    math_group = init_parser.add_argument_group(title="math options")

    # Package "mathtools"
    math_group.add_argument("--mathtools", action="store_true", help="Include 'mathtools' package")

    # Theorem environments
    math_group.add_argument("--theoremstyle", choices=get_choices("theoremstyles"), help="Theorem style to use for the document")
    math_group.add_argument("--theoremsparent", default="section", help="Parent for the numbering of the theorem environments")

    # Macros
    macros_group = init_parser.add_argument_group(title="macros options")
    macros_group.add_argument("--macros", nargs="*", choices=get_choices("macros"), help="Macros to include for the project")

    # "template" subcommand
    template_parser = subparsers.add_parser("template", help="Initialize a project using a template")
    template_parser.add_argument("template", choices=get_choices("templates"), help="Template to use for the project")

    return parser

def parse_args(args, parser=get_parser()):
    args = parser.parse_args(args)
    
    if args.subcommand == "init":
        return args
    elif args.subcommand == "template":
        template = get_template(args.template)
        return parser.parse_args(["-p", args.path, "-n", args.name, "-l", args.language, "init"] + template)
