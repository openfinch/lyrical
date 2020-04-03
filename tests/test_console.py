# tests/test_console.py
import click.testing
import pytest

from lyrical import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_musicbrainz_search(mocker):
    return mocker.patch("lyrical.musicbrainz.search")


def test_main_succeeds(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_main_returns_search_feature_helper(runner):
    result = runner.invoke(console.main)
    assert "search" in result.output
    assert "analyse" in result.output


def test_search_succeeds_using_mock_simple(runner, mock_requests_get):
    result = runner.invoke(console.search, ["--name", "The Cure"])
    assert "The Cure" in result.output
    assert "The Cure, 1977 (Crawley, GB)" in result.output


@pytest.mark.e2e
def test_search_succeeds_using_api_simple(runner):
    result = runner.invoke(console.search, ["--name", "The Cure"])
    assert "The Cure" in result.output
    assert "The Cure, 1977 (Crawley, GB)" in result.output
