"""Config class and functions."""
from pathlib import Path
import yaml

import click

from customtex.defaults import TEMPLATES_FOLDER, CONFIG_FILE, DEFAULT_CONFIG


class Config:
    """Configuration class."""
    default_context: dict

    def __init__(self, **kwargs) -> None:
        """Initialize the configuration."""
        self.default_context = kwargs

    def echo(self) -> None:
        """Return a string representation of the configuration."""
        for key, value in self.default_context.items():
            click.echo(f"{key}: {value}")

    @staticmethod
    def load(path: Path) -> "Config":
        """Load the configuration from a file."""
        with open(path) as config_file:
            config_dict = yaml.safe_load(config_file)
            return Config(**config_dict["default_context"])

    def save(self, path: Path) -> None:
        """Save the configuration to a file."""
        config_content = {"default_context": self.default_context}
        with open(path, "w") as config_file:
            yaml.dump(config_content, config_file)
        
    def edit(self) -> None:
        """Edit the configuration."""
        for key, value in self.default_context.items():
            self.default_context[key] = click.prompt(
                click.style(f"{key}:", fg="blue"), 
                default=value
            )



def setup_config_dir(path: Path) -> Path:
    """Create the configuration directory."""
    path.mkdir(parents=True, exist_ok=True)
    (path / TEMPLATES_FOLDER).mkdir(parents=True, exist_ok=True)

    default_config = Config(**DEFAULT_CONFIG)
    default_config.save(path / CONFIG_FILE)

    return path
