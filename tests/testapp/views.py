from django_renderpdf.views import PDFView


class PromptDownloadView(PDFView):
    template_name = 'test_template.html'
    prompt_download = True
    download_name = 'myfile.pdf'


class NoPromptDownloadView(PDFView):
    template_name = 'test_template.html'
    prompt_download = False


class AllowForceHtmlView(PDFView):
    template_name = 'test_template.html'
    allow_force_html = True


class DisallowForceHtmlView(PDFView):
    template_name = 'test_template.html'
    allow_force_html = False


class TemplateWithStaticFileView(PDFView):
    template_name = 'test_template_with_staticfile.html'
