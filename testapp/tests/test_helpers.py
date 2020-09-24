from unittest.mock import patch

import pytest

from django_renderpdf import helpers
from django_renderpdf.helpers import InvalidRelativeUrl


def test_static_relative_fetched():
    fetched = helpers.django_url_fetcher("/static/styles.css")
    assert fetched == {
        "string": b"html { margin: 0; }\n",
        "mime_type": "text/css",
    }


def test_static_relative_not_found():
    with pytest.raises(InvalidRelativeUrl):
        helpers.django_url_fetcher("/static/non-existent.css")


def test_relative_staticfile_fetched():
    # Manifest files normally won't be found by a finder, but will be present in the
    # staticfiles storage.
    #
    # Patch `find()` to simulate exactly that:
    with patch(
        "django.contrib.staticfiles.finders.find",
        return_value=None,
        spec=True,
    ):
        fetched = helpers.django_url_fetcher("/static/styles.css")
        assert fetched == {
            "string": b"html { margin: 0; }\n",
            "mime_type": "text/css",
        }


def test_relative_url_resolves():
    fetched = helpers.django_url_fetcher("/view.css")
    fetched == {
        "string": b"* { background-color: red; }",
        "mime_type": "text/css",
    }


def test_bogus_relative_url_raises():
    with pytest.raises(InvalidRelativeUrl):
        helpers.django_url_fetcher("/non-existant.css")


def test_absolute_path_resolves():
    mocked_file = {"mime_type": "text/css", "string": "* { font-size: 100px; }"}

    with patch(
        "django_renderpdf.helpers.default_url_fetcher",
        return_value=mocked_file,
        spec=True,
    ) as default_fetcher:
        fetched = helpers.django_url_fetcher("https://example.com/style.css")

    assert default_fetcher.call_count == 1
    assert fetched == {"mime_type": "text/css", "string": "* { font-size: 100px; }"}
