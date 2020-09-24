from django.http import HttpResponse
from django.views.generic import View

from django_renderpdf.views import PDFView


class PromptDownloadView(PDFView):
    template_name = "test_template.html"
    prompt_download = True
    download_name = "myfile.pdf"


class NoPromptDownloadView(PDFView):
    template_name = "test_template.html"
    prompt_download = False


class AllowForceHtmlView(PDFView):
    template_name = "test_template.html"
    allow_force_html = True


class DisallowForceHtmlView(PDFView):
    template_name = "test_template.html"
    allow_force_html = False


class TemplateWithStaticFileView(PDFView):
    template_name = "test_template_with_staticfile.html"


class CssView(View):
    """Test view that returns some CSS."""

    def get(self, request):
        return HttpResponse("* { background-color: red; }")


class NoTemplateDefinedView(PDFView):
    """A view that's missing a template_name."""


class PromptWithMissingDownloadNameView(PDFView):
    template_name = "test_template.html"
    prompt_download = True
