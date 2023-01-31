from unittest.mock import call
from unittest.mock import patch

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory
from django.test import TestCase

from django_renderpdf.views import PDFView
from testapp import views

factory = RequestFactory()


class PromptDownloadTestCase(TestCase):
    def test_prompt_download(self):
        request = factory.get("/some_view")

        response = views.PromptDownloadView.as_view()(request)
        assert response.status_code == 200
        assert (
            b"Content-Type: application/pdf"
            in response.serialize_headers().splitlines()
        )
        assert (
            b'Content-Disposition: attachment; filename="myfile.pdf"'
            in response.serialize_headers().splitlines()
        )
        # Assert that response looks like a PDF
        assert response.content.startswith(b"%PDF-1.") is True

    def test_dont_prompt_download(self):
        request = factory.get("/some_view")

        response = views.NoPromptDownloadView.as_view()(request)
        assert response.status_code == 200
        assert (
            b"Content-Type: application/pdf"
            in response.serialize_headers().splitlines()
        )
        assert b"Content-Disposition:" not in response.serialize_headers()
        # Assert that response looks like a PDF
        assert response.content.startswith(b"%PDF-1.") is True


class ForceHTMLTestCase(TestCase):
    def test_force_html_allowed(self):
        request = factory.get("/some_view?html=true")

        response = views.AllowForceHtmlView.as_view()(request)
        assert response.status_code == 200
        assert response.content == b"Hi!\n"
        assert (
            b"Content-Type: text/html; charset=utf-8"
            in response.serialize_headers().splitlines()
        )

    def test_no_force_html_allowed(self):
        request = factory.get("/some_view")

        response = views.AllowForceHtmlView.as_view()(request)
        assert response.status_code == 200
        assert (
            b"Content-Type: application/pdf"
            in response.serialize_headers().splitlines()
        )
        # Assert that response looks like a PDF
        assert response.content.startswith(b"%PDF-1.") is True

    def test_force_html_disallowed(self):
        request = factory.get("/some_view?html=true")

        response = views.DisallowForceHtmlView.as_view()(request)
        assert response.status_code == 200
        assert (
            b"Content-Type: application/pdf"
            in response.serialize_headers().splitlines()
        )
        # Assert that response looks like a PDF
        assert response.content.startswith(b"%PDF-1.") is True

    def test_no_force_html_disallowed(self):
        request = factory.get("/some_view")

        response = views.DisallowForceHtmlView.as_view()(request)
        assert response.status_code == 200
        assert (
            b"Content-Type: application/pdf"
            in response.serialize_headers().splitlines()
        )
        # Assert that response looks like a PDF
        assert response.content.startswith(b"%PDF-1.") is True


class CustomUrlFetcherTestCase(TestCase):
    pass  # TODO


class StaticFileResolutionTestCase(TestCase):
    def test_url_fetcher_used(self):
        request = factory.get("/some_view")

        with patch(
            "django_renderpdf.helpers.django_url_fetcher",
            return_value={
                "string": "html { margin: 0; }",
                "mime_type": "text/css",
            },
            spec=True,
        ) as fetcher:
            response = views.TemplateWithStaticFileView.as_view()(request)

        assert response.status_code == 200
        assert fetcher.call_count == 1
        assert fetcher.call_args == call("/static/path/not/relevant.css")


def test_view_with_no_template(rf):
    request = factory.get("/test")

    with pytest.raises(
        ImproperlyConfigured,
        match=r"requires either a definition of.*template_name.*get_template_names",
    ):
        views.NoTemplateDefinedView.as_view()(request)


def test_view_with_missing_download_name(rf):
    request = factory.get("/test")

    with pytest.raises(
        ImproperlyConfigured,
        match=r"requires.*download_name",
    ):
        views.PromptWithMissingDownloadNameView.as_view()(request)


def test_view_with_multiple_template_names(rf):
    class TestView(PDFView):
        def get_template_names(self):
            return [
                "test_template.html",
                "test_template.html",
            ]

    request = factory.get("/test")
    response = TestView.as_view()(request)

    assert response.status_code == 200
