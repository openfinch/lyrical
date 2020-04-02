# tests/test_console.py
import click.testing
import pytest

from lyrical import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()

def test_main_succeeds(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0

def test_main_returns_help_string(runner):
    result = runner.invoke(console.main)
    assert 'Usage: lyrical [OPTIONS] COMMAND [ARGS]' in result.output

def test_main_returns_search_feature_helper(runner):
    result = runner.invoke(console.main)
    assert 'search  Search the Musicbrainz database by artist.' in result.output


def test_search_succeeds(runner):
    result = runner.invoke(console.search)
    assert result.exit_code == 0

def test_search_returns_simple_search_result(runner):
    result = runner.invoke(console.search, ['The Cure'])
    assert result.output == 'The Cure\nThe Cure, 1977 (Crawley, GB)'