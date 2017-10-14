from unittest.mock import call, MagicMock, patch

from django.test import TestCase

from django_renderpdf import helpers


class StaticFilesUrlFetcherTestCase(TestCase):
    def test_relative_path(self):
        file_ = helpers.staticfiles_url_fetcher('/static/styles.css')
        self.assertEqual(
            file_,
            {
                'string': b'html { margin: 0; }\n',
                'mime_type': 'text/css',
            },
        )

    def test_absolute_path(self):
        mocked_file = MagicMock()

        with patch(
            'django_renderpdf.helpers.default_url_fetcher',
            return_value=mocked_file,
            spec=True,
        ) as default_fetcher:
            file_ = helpers.staticfiles_url_fetcher(
                'https://example.com/style.css',
            )

        self.assertEqual(default_fetcher.call_count, 1)
        self.assertEqual(
            default_fetcher.call_args,
            call('https://example.com/style.css'),
        )
        self.assertEqual(file_, mocked_file)
