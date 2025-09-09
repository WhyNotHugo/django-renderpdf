import io
from unittest.mock import patch

import pytest
from django.conf import settings
from django.template.exceptions import TemplateDoesNotExist

from django_renderpdf import helpers
from django_renderpdf.helpers import InvalidRelativeUrl


def test_static_relative_fetched() -> None:
    fetched = helpers.django_url_fetcher("/static/styles.css")
    assert fetched == {
        "string": b"html { margin: 0; }\n",
        "mime_type": "text/css",
    }


def test_static_relative_not_found() -> None:
    with pytest.raises(InvalidRelativeUrl):
        helpers.django_url_fetcher("/static/non-existent.css")


def test_relative_staticfile_fetched() -> None:
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


def test_relative_url_resolves() -> None:
    fetched = helpers.django_url_fetcher("/view.css")
    assert fetched == {
        "string": b"* { background-color: red; }",
        "mime_type": "text/css",
    }


def test_bogus_relative_url_raises() -> None:
    with pytest.raises(InvalidRelativeUrl):
        helpers.django_url_fetcher("/non-existant.css")


def test_absolute_path_resolves() -> None:
    mocked_file = {"mime_type": "text/css", "string": "* { font-size: 100px; }"}

    with patch(
        "django_renderpdf.helpers.default_url_fetcher",
        return_value=mocked_file,
        spec=True,
    ) as default_fetcher:
        fetched = helpers.django_url_fetcher("https://example.com/style.css")

    assert default_fetcher.call_count == 1
    assert fetched == {"mime_type": "text/css", "string": "* { font-size: 100px; }"}


def test_render_pdf_single_template() -> None:
    file_ = io.BytesIO()
    helpers.render_pdf("test_template.html", file_)

    # TODO: make sure some of the text from the template is actually in the PDF?
    #       this would benefit from some manual validation mechanism.
    data = file_.getvalue()
    assert data.startswith(b"%PDF-1.7\n")
    assert len(data) > 2000


def test_render_pdf_several_templates() -> None:
    file_ = io.BytesIO()
    helpers.render_pdf(
        ["test_template.html", "test_template_with_staticfile.html"],
        file_,
    )

    assert len(file_.getvalue()) > 2000


def test_render_pdf_with_some_non_existant() -> None:
    file_ = io.BytesIO()
    helpers.render_pdf(["idontexist.html", "test_template.html"], file_)

    # Pdf for this template should be about 8kB
    assert len(file_.getvalue()) > 2000


def test_render_pdf_with_non_existant() -> None:
    file_ = io.BytesIO()

    with pytest.raises(TemplateDoesNotExist):
        helpers.render_pdf(["idontexist.html"], file_)


def test_render_pdf_with_merged_options() -> None:
    global_options = {
        "zoom": 1.0,
        "presentational_hints": True,
        "optimize_images": False,
        "jpeg_quality": 85,
        "dpi": 96,
        "pdf_version": "1.7",
        "uncompressed_pdf": True,
        "attachments": None,
        "pdf_forms": False,
        "hinting": False,
        "cache": None,
    }
    local_options = {"jpeg_quality": 90, "cache": "memory"}
    expected_options = {**global_options, **local_options}
    file_ = io.BytesIO()
    with (
        patch.object(settings, "WEASYPRINT_OPTIONS", global_options),
        patch("django_renderpdf.helpers.HTML.write_pdf") as mock_write_pdf,
    ):
        helpers.render_pdf("test_template.html", file_, options=local_options)
        mock_write_pdf.assert_called_once_with(target=file_, **expected_options)
