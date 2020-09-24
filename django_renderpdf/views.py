from typing import Optional

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import View
from django.views.generic.base import ContextMixin

from django_renderpdf import helpers


class PDFView(View, ContextMixin):
    """A base class that renders requests as PDF files.

    All views that render a PDF must inherit from this base class.

    Usage and interface is quite similar to Django's built-in views. Template
    context data can be defined via ``get_context_data`` just like with
    Django's ``TemplateView`` subclasses.

    The following additional attributes allow further customising behaviour of
    subclasses. These may be overridden by either an attribute or a property:

    .. autoattribute:: template_name

        The name of the template file that will be rendered into a PDF file. Template
        discovery works just like any regular Django view.

    .. autoattribute:: allow_force_html

        Allow forcing this view to return a rendered HTML response, rather than a PDF
        response.  If ``True``, any requests with the URL parameter ``html=true`` will
        be rendered as plain HTML. This can be useful during development, but may be
        desirable in some production scenarios.

    .. autoattribute:: prompt_download

        If ``True``, users will be prompted to download the PDF file, rather than have
        it rendered by their browsers.

    .. autoattribute:: download_name

        The filename with which users will be prompted to save this file as by default.
        This can be overridden by defining ``get_download_name``.

        Only required if ``prompt_download = True``.

    The following methods may also be overridend to further customise subclasses:

    .. automethod:: url_fetcher
    .. automethod:: get_download_name
    """

    template_name: Optional[str] = None
    allow_force_html: bool = True
    prompt_download: bool = False
    download_name: Optional[str] = None

    def url_fetcher(self, url):
        """Returns the file matching URL.

        This method will handle any URL resources that rendering HTML requires
        (e.g.: images in ``img`` tags, stylesheets, etc.).

        The default behaviour will fetch any http(s) files normally, and will
        also attempt to resolve staticfiles internally.

        See :func:`django_renderpdf.helpers.url_fetcher` for further details.
        """
        return helpers.django_url_fetcher(url)

    def get_download_name(self) -> str:
        """Return the default filename when this file is downloaded.

        Users will only be prompted to download the PDF file if ``prompt_download`` is
        ``True``, otherwise, browsers will generally render it.
        """
        if self.download_name is None:
            raise ImproperlyConfigured(
                "PDFView with 'prompt_download=True' requires either a "
                "definition of 'download_name' or an impementation of "
                "'get_download_name'."
            )
        else:
            return self.download_name

    def get_template_name(self) -> str:
        """Return the name of the template which will be rendered into a PDF."""
        if self.template_name is None:
            raise ImproperlyConfigured(
                "PDFView requires either a definition of 'template_name' or "
                "an impementation of 'get_template_name'."
            )
        else:
            return self.template_name

    def render(self, request, template, context) -> HttpResponse:
        """Returns a response.

        By default, this will contain the rendered PDF, but if both ``allow_force_html``
        is ``True`` and the querystring ``html=true`` was set it will return a plain
        HTML.
        """
        if self.allow_force_html and self.request.GET.get("html", False):
            html = get_template(template).render(context)
            return HttpResponse(html)
        else:
            response = HttpResponse(content_type="application/pdf")
            if self.prompt_download:
                response["Content-Disposition"] = 'attachment; filename="{}"'.format(
                    self.get_download_name()
                )
            helpers.render_pdf(
                template=template,
                file_=response,
                url_fetcher=self.url_fetcher,
                context=context,
            )
            return response

    # Move all the above into BasePdfView, which can be subclassed for posting
    def get(self, request, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(*args, **kwargs)
        return self.render(
            request=request,
            template=self.get_template_name(),
            context=context,
        )
