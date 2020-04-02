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
    assert 'Usage: main [OPTIONS] COMMAND [ARGS]' in result.output

def test_main_returns_search_feature_helper(runner):
    result = runner.invoke(console.main)
    assert 'search  Search the Musicbrainz database by artist.' in result.output

def test_search_returns_simple_search_result(runner):
    result = runner.invoke(console.search, ['--name','The Cure'])
    assert 'The Cure' in result.output
    assert 'The Cure, 1977 (Crawley, GB)' in result.output