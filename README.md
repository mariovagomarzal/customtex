# CustomTeX v0.1.1

### A CLI utility for setting up LaTeX projects
CustomTeX is a command line utility for setting up LaTeX projects based on some predefined styles for titles, section headers, theorems, etc.

For the moment, the utility is intended for a personal use, since there aren't many options for customization. However, we aim to design a more general system for creating LaTeX projects based on dynamic and fully customizable templates.

## Installation
CustomTeX is a Python library and can be installed using pip:

    pip install customtex

No additional dependencies are required.

## Usage
To generate the main files of a LaTeX project with CustomTeX, you have to run the `customtex` command followed by the path, main file name and language options and the `init` or the `template` subcommand. For example:

    customtex --path /path/to/directory --name main --lang english init [options]

This will create a LaTeX project with the following structure in the `path/to/directory` directory:

    /path/to/directory
    ├── main.tex
    └── tex
        ├── macros.tex
        └── preamble.tex


### The `init` subcommand
The `init` subcommand creates a project based on the options that the utility provides. Run `customtex init --help` to see the available options.

### The `template` subcommand
The `template` subcommand creates a project based on a template. A template consist of a list of options from the `init` subcommand that are run when invoking the `template` option followed by the name of the template.

Run `customtex template --help` to see the available templates.

## License
CustomTeX is licensed under the MIT license. See the LICENSE file for more information.
