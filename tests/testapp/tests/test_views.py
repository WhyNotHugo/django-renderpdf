from django.test import RequestFactory, TestCase

from testapp import views

factory = RequestFactory()


class PromptDownloadTestCase(TestCase):

    def test_prompt_download(self):
        request = factory.get('/some_view')

        response = views.PromptDownloadView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Content-Type: application/pdf',
            response.serialize_headers().splitlines()
        )


class ForceDownloadTestCase(TestCase):
    pass


class CustomUrlFetcherTestCase(TestCase):
    pass


class StaticFileResolutionTestCase(TestCase):
    pass
