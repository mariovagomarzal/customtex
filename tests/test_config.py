"""Tests for the 'config' module."""
from pathlib import Path

import pytest

from customtex.config import Config, setup_config_dir
from customtex.defaults import TEMPLATES_FOLDER, CONFIG_FILE

# Helper functions and fixtures
@pytest.fixture
def fake_config_dir() -> Path:
    """Return a fake config directory."""
    return Path(__file__).parent / "fake_config_dir"


# Tests
def test_config_load(fake_config_dir: Path):
    """Test the 'load' method of the 'Config' class."""
    config = Config().load(fake_config_dir / "config.yaml")
    assert config.default_context["author"] == "Example Name"
    assert config.default_context["title"] == "Example title"

def test_config_save(tmp_path: Path):
    """Test the 'save' method of the 'Config' class."""
    config = Config(author="Example Name", title="Example title")
    config.save(tmp_path / "config.yaml")

    with open(tmp_path / "config.yaml", "r") as f:
        config_yaml = f.read()

    assert "default_context:" in config_yaml
    assert "author: Example Name" in config_yaml
    assert "title: Example title" in config_yaml

def test_config_edit(fake_config_dir: Path, monkeypatch):
    """Test the 'edit' method of the 'Config' class."""
    # TODO

def test_setup_config_dir(tmp_path: Path):
    """Test the 'setup_config_dir' function."""
    path = setup_config_dir(tmp_path / "config")
    assert (path / TEMPLATES_FOLDER).exists()
    assert (path / CONFIG_FILE).exists()
    assert (path / CONFIG_FILE).is_file()
