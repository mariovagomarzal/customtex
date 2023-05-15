"""Tests for the CustomTeX CLI module."""
from pathlib import Path

import pytest
from click.testing import CliRunner

from customtex.cli import main


# Helper functions and fixtures
def debug_invoke(cli_runner: CliRunner, *kargs, **kwargs):
    """Invoke the main command with debug mode enabled."""
    return cli_runner.invoke(main, ["--debug", *kargs], **kwargs)


@pytest.fixture
def cli_runner():
    """Return CliRunner."""
    return CliRunner()


# Tests
def test_main_version(cli_runner: CliRunner):
    """Test the 'version' command."""
    result_version = debug_invoke(cli_runner, "--version")
    result_v = debug_invoke(cli_runner, "-v")

    assert result_version.exit_code == 0
    assert result_v.exit_code == 0
    assert "CustomTeX" in result_version.output
    assert "CustomTeX" in result_v.output


def test_new_no_config_success(cli_runner: CliRunner):
    """Test the 'new' command."""
    result = debug_invoke(
        cli_runner,
        "new",
        "--project-slug=example"
        "--author=John Doe",
        "--title=Example Document",
        "--date=\\today",
        "--language=english",
        "--no-config"
    )

    assert result.exit_code == 0


def test_new_config_success(cli_runner: CliRunner, tmp_path: Path):
    """Test the 'new' command."""
    with cli_runner.isolated_filesystem(temp_dir=tmp_path):
        Path(".customtex").mkdir()
        Path(".customtex/config.yaml").touch()
        result = debug_invoke(
            cli_runner,
            "new",
            "--config"
        )

    assert result.exit_code == 0
