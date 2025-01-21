import datetime
import pytest
from tactics_manager import (
    determine_next_theme,
    get_theme_difficulty,
    update_theme_difficulty_progress,
    days_since,
    THEMES_BY_CATEGORY,
    DIFFICULTY_LEVELS,
)


# Mock Data
def mock_date(days_ago):
    """Generate a date string for `days_ago` days in the past."""
    return (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime(
        "%Y-%m-%d"
    )


@pytest.fixture
def mock_data():
    data = {"themes": {}}
    for category, themes in THEMES_BY_CATEGORY.items():
        for theme in themes:
            data["themes"][theme] = {
                "last_attempted": None,
                "success_rate": None,
                "difficulty_progress": {
                    level: {"puzzles_solved": 0, "correct": 0}
                    for level in DIFFICULTY_LEVELS
                },
            }
    # Customize specific themes for testing
    data["themes"]["Fork"] = {
        "last_attempted": mock_date(150),
        "success_rate": 8,
        "difficulty_progress": {
            level: {"puzzles_solved": 0, "correct": 0} for level in DIFFICULTY_LEVELS
        },
    }
    data["themes"]["Pins"] = {
        "last_attempted": mock_date(10),
        "success_rate": 6,
        "difficulty_progress": {
            level: {"puzzles_solved": 0, "correct": 0} for level in DIFFICULTY_LEVELS
        },
    }
    data["themes"]["Skewers"] = {
        "last_attempted": mock_date(5),
        "success_rate": 6,
        "difficulty_progress": {
            level: {"puzzles_solved": 0, "correct": 0} for level in DIFFICULTY_LEVELS
        },
    }
    return data


def test_days_since():
    assert days_since(mock_date(0)) == 0
    assert days_since(mock_date(10)) == 10
    assert days_since(None) == float("inf")  # Never attempted case


def test_determine_next_theme(mock_data):
    data = mock_data
    # The first unmastered theme in the theme order is 'Discovered attack'
    assert (
        determine_next_theme(data) == "Discovered attack"
    )  # Prioritize unmastered themes

    # Simulate mastering 'Discovered attack'
    data["themes"]["Discovered attack"]["success_rate"] = 8
    assert (
        determine_next_theme(data) == "Pin"
    )  # Now prioritize the next unmastered theme


def test_get_theme_difficulty(mock_data):
    data = mock_data
    theme = "Fork"
    assert get_theme_difficulty(data, theme) == "Easiest"  # Starts with the first level

    # Simulate completing the first level
    data["themes"][theme]["difficulty_progress"]["Easiest"] = {
        "puzzles_solved": 50,
        "correct": 40,
    }
    assert get_theme_difficulty(data, theme) == "Easier"


def test_update_theme_difficulty_progress(mock_data):
    data = mock_data
    theme = "Fork"

    # Update progress with correct answers
    update_theme_difficulty_progress(data, theme, correct=True)
    assert (
        data["themes"][theme]["difficulty_progress"]["Easiest"]["puzzles_solved"] == 1
    )
    assert data["themes"][theme]["difficulty_progress"]["Easiest"]["correct"] == 1

    # Update progress with an incorrect answer
    update_theme_difficulty_progress(data, theme, correct=False)
    assert (
        data["themes"][theme]["difficulty_progress"]["Easiest"]["puzzles_solved"] == 2
    )
    assert data["themes"][theme]["difficulty_progress"]["Easiest"]["correct"] == 1


def test_theme_difficulty_completion(mock_data):
    data = mock_data
    theme = "Fork"

    # Simulate completing all levels
    for level in DIFFICULTY_LEVELS:
        data["themes"][theme]["difficulty_progress"][level] = {
            "puzzles_solved": 50,
            "correct": 50,
        }
    assert get_theme_difficulty(data, theme) is None  # All levels completed
