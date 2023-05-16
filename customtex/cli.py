"""CustomTeX command-line interface."""
import json
import sys
from pathlib import Path

import click
from cookiecutter.main import cookiecutter

from customtex import __version__
from customtex.config import setup_config_dir
from customtex.defaults import (
    COOKIECUTTER_TEMPLATE,
    CUSTOMTEX_FOLDER,
    get_langs,
    set_main_language,
)


# Auxiliary and echo functions
def echo_info(msg: str):
    """Print an info message."""
    click.echo(click.style(msg, fg="blue"))

def echo_success(msg: str):
    """Print a success message."""
    click.echo(click.style(msg, fg="green"))

def echo_warning(msg: str):
    """Print a warning message."""
    click.echo(click.style(msg, fg="yellow"))

def echo_error(msg: str):
    """Print an error message."""
    click.echo(click.style(msg, fg="red"))

def confirm_reset() -> bool:
    """Confirm reset of user configuration."""
    return click.confirm(
        click.style(
            "Are you sure you want to reset your configuration?", 
            fg="yellow"
        ),
        abort=True
    )


def version_msg():
    """Return the CustomTeX version, location and Python powering it."""
    python_version = sys.version
    location = Path(__file__).resolve().parent.parent
    return f"CustomTeX {__version__} from {location} (Python {python_version})"



# Main command for 'customtex'
@click.group()
@click.help_option("-h", "--help")
@click.version_option(__version__, "-v", "--version", message=version_msg())
@click.option("--debug", is_flag=True, hidden=True, help="Enable debug mode.")
@click.option("--reset", is_flag=True, help="Reset user configuration.")
@click.option(
    "--config-dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Use a custom configuration directory."
)
@click.pass_context
def main(ctx, debug: bool, reset: bool, config_dir: Path):
    """CustomTeX is a CLI utility for setting up LaTeX projects."""
    ctx.ensure_object(dict)

    ctx.obj["DEBUG"] = debug

    # Handle configuration directory preferences
    if not config_dir and not debug:
        ctx.obj["CONFIG_DIR"] = CUSTOMTEX_FOLDER

        # Handle creation of configuration directory
        if reset:
            reset = confirm_reset()

        if not CUSTOMTEX_FOLDER.exists() or reset:
            echo_info("Configuration directory is going to be created.")
            setup_config_dir(CUSTOMTEX_FOLDER)
            echo_success(f"Created configuration directory at {CUSTOMTEX_FOLDER}.")
    else:
        if config_dir:
            ctx.obj["CONFIG_DIR"] = config_dir
        else: # If debug, but no config_dir is given
            ctx.obj["CONFIG_DIR"] = Path().cwd() / ".customtex" # Testing purposes
        echo_info(f"Using custom configuration directory at {config_dir}.")

    if ctx.invoked_subcommand is None:
        sys.exit(0)


# 'new' subcommand
@main.command(help="Create a new LaTeX project.")
@click.option(
    "--template", "-t",
    type=click.STRING, 
    help="Template (or 'context') to use."
)
@click.option("--project-slug", type=click.STRING, help="Directory name.")
@click.option("--author", type=click.STRING, help="Author name.")
@click.option("--title", type=click.STRING, help="Document title.")
@click.option("--date", type=click.STRING, help="Document date.")
@click.option("--language", type=click.Choice(get_langs()), help="Document language.")
@click.option("--config/--no-config", default=True, help="Use user configuration.")
@click.option(
    "--prompt/--no-prompt", 
    default=False, 
    help="Prompt for template variables."
)
@click.option("--overwrite", is_flag=True, help="Overwrite existing files.")
@click.argument("output_dir", default=Path("."), type=click.Path(path_type=Path))
@click.pass_context
def new(
    ctx,
    template: str,
    project_slug: str,
    author: str,
    title: str,
    date: str,
    language: str,
    config: bool, 
    prompt: bool, 
    overwrite: bool, 
    output_dir: Path
):
    """Create a new CustomTeX project."""
    # Handle extra context for the template generation
    extra_context = {}

    # Get extra context if template is specified
    if template:
        templates_dir = ctx.obj["CONFIG_DIR"] / "templates"
        template_path = templates_dir / (template + ".json")
        if template_path.exists():
            with open(template_path) as template_file:
                extra_context = json.load(template_file)
            echo_info(f"Using template '{template}' for extra context.")
        else:
            echo_error(f"Template '{template}' does not exist.")
            sys.exit(1)

    # Override extra context with command-line arguments
    if project_slug:
        extra_context["project_slug"] = project_slug
    if author:
        extra_context["author"] = author
    if title:
        extra_context["title"] = title
    if date:
        extra_context["date"] = date
    if language:
        extra_context["language"] = set_main_language(language)

    # Handle configuration file
    if config:
        config_file = ctx.obj["CONFIG_DIR"] / "config.yaml"
        if not config_file.exists():
            echo_error(f"Configuration file '{config_file}' does not exist.")
            sys.exit(1)
        else:
            echo_info(f"Using configuration file '{config_file}'.")
    else:
        config_file = None

    # Override possible output directory for testing purposes
    if ctx.obj["DEBUG"]:
        output_dir = Path().cwd()

    # Create the project
    echo_info(f"Creating project in '{output_dir}'...")
    result = cookiecutter(
        template=str(COOKIECUTTER_TEMPLATE),
        no_input=not prompt,
        extra_context=extra_context,
        overwrite_if_exists=overwrite,
        config_file=config_file,
        output_dir=str(output_dir),
    )

    # Due to a bug in cookiecutter with the jinja2 delimiters, 
    # the project directory is created with '{{' and '}}' in the name.
    # This is a workaround to fix that.
    project_dir = Path(result)
    if project_dir.name.startswith("{{") and project_dir.name.endswith("}}"):
        project_dir = project_dir.rename(
            project_dir.parent / project_dir.name[2:-2]
        )

    echo_success(f"Project created successfully at {project_dir}.")

    sys.exit(0)


# 'config' subcommand
@main.command()
@click.pass_context
def config(ctx):
    """Manage configuration file (of the given configuration directory)."""
    # TODO: Implement
    pass
