from typing import List
from typing import Optional

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.template.loader import select_template
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
        be rendered as plain HTML. This can be useful for debugging, but also allows
        reusing the same view for exposing both PDFs and HTML.

    .. autoattribute:: prompt_download

        If ``True``, users will be prompted to download the PDF file, rather than have
        it rendered by their browsers.

        This is achieved by setting the "Content-Disposition" HTTP header. If this
        attribute is ``True``, then either :attr:`~download_name` or
        :func:`~get_download_name` must be defined.

    .. autoattribute:: download_name

        When ``prompt_download`` is set to ``True``, browsers will be instructed to
        prompt users to download the file, rather than render it.

        In these cases, a default filename is presented. If you need custom filenames,
        you may override this attribute with a property:

        .. code:: python

            @property
            def download_name(self) -> str:
                return f"document_{self.request.kwargs['pk']}.pdf"

        This attribute has no effect if ``prompt_download = False``.

    The following methods may also be overridden to further customise subclasses:

    .. automethod:: url_fetcher
    .. automethod:: get_template_names
    .. automethod:: get_download_name
    .. automethod:: get_template_name
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
        also attempt to resolve relative URLs internally.

        Generally, you should not need to override this method unless you want to use
        custom URL schemes. For finer details on its inner workings, see
        `weasyprint's documentation on url_fetcher`_.

        .. _weasyprint's documentation on url_fetcher: https://weasyprint.readthedocs.io/en/stable/tutorial.html#url-fetchers
        """  # noqa: E501
        return helpers.django_url_fetcher(url)

    def get_download_name(self) -> str:
        """Return the default filename when this file is downloaded.

        .. deprecated:: 3.0

            Use :func:`~download_name` as a property instead.
        """
        if self.download_name is None:
            raise ImproperlyConfigured(
                "PDFView with 'prompt_download=True' requires a definition "
                "of 'download_name'."
            )
        else:
            return self.download_name

    def get_template_names(self) -> List[str]:
        """Return a list of template names to be used for the request.

        Must return a list. By default, just returns ``[self.template_name]``.

        .. versionadded:: 3.0
        """
        return [self.get_template_name()]

    def get_template_name(self) -> str:
        """Return the name of the template which will be rendered into a PDF.

        .. deprecated:: 3.0

            Use :func:`~get_template_names` instead.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "PDFView requires either a definition of 'template_name' or "
                "an impementation of 'get_template_names()'."
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
            html = select_template(template).render(context)
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
            template=self.get_template_names(),
            context=context,
        )
