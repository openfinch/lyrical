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


@pytest.mark.e2e
def test_search_succeeds_using_api_fuzzy_match(runner):
    result = runner.invoke(console.search, ["--name", "Billy Eilish"])
    assert "Billy Eilish" not in result.output
    assert "Billie Eilish, 2001-12-18 (Los Angeles, US)" in result.output


@pytest.mark.e2e
def test_search_succeeds_using_api_tracklist(runner):
    result = runner.invoke(console.search, ["--name", "Billie Eilish", "--tracklist"])
    assert "Billie Eilish" in result.output
    assert "Billie Eilish, 2001-12-18 (Los Angeles, US)" in result.output
    assert "bad guy" in result.output


def test_analyse_succeeds(runner):
    result = runner.invoke(console.analyse, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_analyse_fails_on_nonexistent_analysis(runner):
    result = runner.invoke(
        console.analyse, ["--name", "Billie Eilish", "--analysis=fake"]
    )
    assert result.exit_code == 1
    assert "Analysis not recognised" in result.output


def test_analyse_returns_wordcounts_for_all(runner):
    result = runner.invoke(
        console.analyse, ["--name", "Billie Eilish", "--analysis=all"]
    )
    assert result.exit_code == 0
    assert "Average" in result.output


def test_analyse_returns_wordcounts_for_wordcount(runner):
    result = runner.invoke(
        console.analyse, ["--name", "Billie Eilish", "--analysis=wordcount"]
    )
    assert result.exit_code == 0
    assert "Average" in result.output


def test_analyse_succeeds_using_mock_simple(runner, mock_requests_get):
    result = runner.invoke(console.analyse, ["--name", "The Cure"])
    assert "The Cure" in result.output
    assert "The Cure, 1977 (Crawley, GB)" in result.output


# @pytest.mark.e2e
# def test_search_succeeds_using_api_simple(runner):
#     result = runner.invoke(console.search, ["--name", "The Cure"])
#     assert "The Cure" in result.output
#     assert "The Cure, 1977 (Crawley, GB)" in result.output

# @pytest.mark.e2e
# def test_search_succeeds_using_api_fuzzy_match(runner):
#     result = runner.invoke(console.search, ["--name", "Billy Eilish"])
#     assert "Billy Eilish" not in result.output
#     assert "Billie Eilish, 2001-12-18 (Los Angeles, US)" in result.output

# @pytest.mark.e2e
# def test_search_succeeds_using_api_tracklist(runner):
#     result = runner.invoke(console.search, ["--name", "Billie Eilish", "--tracklist"])
#     assert "Billie Eilish" in result.output
#     assert "Billie Eilish, 2001-12-18 (Los Angeles, US)" in result.output
#     assert "bad guy" in result.output
