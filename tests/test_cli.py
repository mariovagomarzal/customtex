"""Tests for the 'cli' module."""
from pathlib import Path

import pytest
from click.testing import CliRunner

from customtex.cli import main


# Helper functions and fixtures
# NOTE: Don't use the 'invoke' function from 'click.testing' without the
#       '--debug' flag. It may create undesired files and folders on the system.
def debug_invoke(cli_runner: CliRunner, *kargs, **kwargs):
    """Invoke the main command with debug mode enabled."""
    return cli_runner.invoke(main, ["--debug", *kargs], **kwargs)


@pytest.fixture
def cli_runner() -> CliRunner:
    """Return CliRunner."""
    return CliRunner()

@pytest.fixture
def fake_config_dir() -> Path:
    """Return a fake config directory."""
    return Path(__file__).parent / "fake_config_dir"


# Tests
def test_main_version(cli_runner: CliRunner):
    """Test the 'version' command."""
    result_version = debug_invoke(cli_runner, "--version")
    result_v = debug_invoke(cli_runner, "-v")

    assert result_version.exit_code == 0
    assert result_v.exit_code == 0
    assert "CustomTeX" in result_version.output
    assert "CustomTeX" in result_v.output


def test_new_without_config(cli_runner: CliRunner, tmp_path: Path):
    """Test the 'new' command."""
    with cli_runner.isolated_filesystem(temp_dir=tmp_path):
        result = debug_invoke(
            cli_runner,
            "new",
            "--project-slug", "test-project",
            "--no-config"
        )

        assert result.exit_code == 0
        assert Path("test-project").exists()
        assert Path("test-project/main.tex").exists()

def test_new_with_config(
    cli_runner: CliRunner, 
    fake_config_dir: Path, 
    tmp_path: Path
):
    """Test the 'new' command with a config directory."""
    with cli_runner.isolated_filesystem(temp_dir=tmp_path):
        result = debug_invoke(
            cli_runner,
            "--config-dir", fake_config_dir,
            "new",
            "--project-slug", "test-project"
        )

        assert result.exit_code == 0
        assert f"{fake_config_dir / 'config.yaml'}" in result.output

        with open("test-project/main.tex", "r") as f:
            main_tex = f.read()

        assert "\\author{Example Name}" in main_tex

def test_new_with_template(
    cli_runner: CliRunner, 
    fake_config_dir: Path, 
    tmp_path: Path
):
    """Test the 'new' command with a template."""
    with cli_runner.isolated_filesystem(temp_dir=tmp_path):
        result = debug_invoke(
            cli_runner,
            "--config-dir", fake_config_dir,
            "new",
            "--project-slug", "test-project",
            "--template", "sample",
            "--no-config"
        )

        assert result.exit_code == 0
        assert "sample" in result.output

        with open("test-project/main.tex", "r") as f:
            main_tex = f.read()

        assert "\\author{Example Name}" in main_tex
