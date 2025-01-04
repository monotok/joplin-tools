import pytest
import responses

import postprocessing.tagger as tagger
from api.joplinapi import JoplinAPI

BASE_URL = "http://127.0.0.1:41184"
TOKEN = "mock_token"


def test_calculate_tags_for_markdown_files():
    actual_tags = tagger.calculate_tags_for_files('resources/notes/', ['md'])
    expected_tags = {'Clean out old kernels': {'tags': ['tech:linux']}, 'Live Patch': {'tags': ['tech:linux', 'tech:ubuntu']},
                     'Move home to ext Drive': {'tags': ['tech:linux', 'tech:ubuntu']}}
    assert actual_tags == expected_tags


@pytest.fixture
def mock_api():
    return JoplinAPI(BASE_URL, TOKEN)


@responses.activate
def test_get_notes_success(mock_api):
    # Mock the API response
    responses.add(
        responses.GET,
        f"{BASE_URL}/notes",
        json={
            "items": [
                {"id": "1", "title": "Note 1", "body": "This is note 1."},
                {"id": "2", "title": "Note 2", "body": "This is note 2."}
            ],
            "has_more": False,
        },
        status=200
    )

    notes = mock_api.get_notes()
    assert len(notes) == 2
    assert notes[0]["title"] == "Note 1"
    assert notes[1]["title"] == "Note 2"


@responses.activate
def test_get_notes_empty(mock_api):
    # Mock an empty response
    responses.add(
        responses.GET,
        f"{BASE_URL}/notes",
        json={"items": [], "has_more": False},
        status=200
    )

    notes = mock_api.get_notes()
    assert notes == []


@responses.activate
def test_get_notes_failure(mock_api):
    # Mock a failure response
    responses.add(
        responses.GET,
        f"{BASE_URL}/notes",
        json={"error": "Invalid token"},
        status=401
    )

    with pytest.raises(Exception, match="Failed to fetch notes: 401"):
        mock_api.get_notes()
