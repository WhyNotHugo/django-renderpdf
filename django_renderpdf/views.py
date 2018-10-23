from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import View
from django.views.generic.base import ContextMixin

from django_renderpdf import helpers


class PDFView(View, ContextMixin):
    """
    A base class that renders requests as PDF files.

    Usage and interface is quite simliar to Django's built-in views. Template
    context data can be defined via ``get_context_data`` just like with
    Django's ``TempalteView`` subclasses. Four class attributes configure extra
    behaviour:


    * ``template_name`` (required): The name of the template file that will be
        rendered into a PDF file.
    * ``allow_force_html`` (default: ``True``): If ``True``, any requests with
        the querystring ``html=true`` will be rendered as plain HTML. This can
        be useful during development, but may be desirable in some production
        scenarios.
    * ``prompt_download`` (default: ``False``): If ``True``, users will be
        prompted to download the PDF file, rather than have it rendered by
        their browsers.
    * ``download_name`` (required if ``prompt_download = True``). The filename
        with which users will be prompted to save this file as by default. This
        can be overriden by defining ``get_download_name``.

    """
    template_name = None
    allow_force_html = True
    prompt_download = False
    download_name = None

    @staticmethod
    def url_fetcher(url):
        """
        Returns the file matching url.

        This method will handle any URL resources that rendering HTML requires
        (eg: images pointed my ``img`` tags, stylesheets, etc).

        The default behaviour will fetch any http(s) files normally, and will
        also attempt to resolve staticfiles internally.

        See ``django_renderpdf.helpers.url_fetcher`` for further details.

        This is a ``@staticmethod``, so if you override it, make sure it's with
        a static method.
        """
        return helpers.staticfiles_url_fetcher(url)

    def get_download_name(self):
        """
        Returns the filename with which users will be prompted to save this
        PDF. Users will only be prompted to download the PDF file if
        ``prompt_download`` is ``True``, otherwise, their browsers render it.

        :rtype str:
        """
        if self.download_name is None:
            raise ImproperlyConfigured(
                "PDFView with 'prompt_download=True' requires either a "
                "definition of 'download_name' or an impementation of "
                "'get_download_name'."
            )
        else:
            return self.download_name

    def get_template_name(self):
        """
        Returns the name of the template which will be rendered into a PDF.

        :rtype str:
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "PDFView requires either a definition of 'template_name' or "
                "an impementation of 'get_template_name'."
            )
        else:
            return self.template_name

    def render(self, request, template, context):
        """
        Returns a response. By default, this will contain the rendered PDF, but
        if both ``allow_force_html`` is ``True`` and the querystring
        ``html=true`` was set it will return a plain HTML.
        """
        if self.allow_force_html and self.request.GET.get('html', False):
            html = get_template(template).render(context)
            return HttpResponse(html)
        else:
            response = HttpResponse(content_type='application/pdf')
            if self.prompt_download:
                response['Content-Disposition'] = 'attachment; filename="{}"' \
                    .format(self.get_download_name())
            helpers.render_pdf(
                template=template,
                file_=response,
                url_fetcher=self.url_fetcher,
                context=context,
            )
            return response

    # Move all the above into BasePdfView, which can be subclassed for posting
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        return self.render(
            request=request,
            template=self.get_template_name(),
            context=context,
        )
