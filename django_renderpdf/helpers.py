import mimetypes
from typing import IO
from typing import List
from typing import Optional
from typing import Union

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http.request import HttpRequest
from django.template.loader import select_template
from django.urls import resolve
from django.urls.exceptions import Resolver404
from weasyprint import default_url_fetcher
from weasyprint import HTML


class InvalidRelativeUrl(ValueError):
    """Raised when a relative URL cannot be handled by Django."""


def django_url_fetcher(url: str):
    """Returns the file for a given URL.

    If the URL appear to be a static file, we will attempt to load it internally.
    Otherwise, it will resolve normally as an external URL.

    Relative URLs are only supported

    The default behaviour will fetch any http(s) files normally, and will
    also attempt to resolve staticfiles internally (this should mostly
    affect development scenarios, but also works if static files are served
    under a relative URL).

    Returns a dictionary with two entries: ``string``, which is the
    resources data as a string and ``mime_type``, which is the identified
    mime type for the resource.
    """
    # If the URL looks like a staticfile, try to load it as such.
    # Reading it from the storage avoids a network call in many cases (unless the
    # storage is remote, in which case this improves nothing:
    try:
        if url.startswith(staticfiles_storage.base_url):
            filename = url.replace(staticfiles_storage.base_url, "", 1)
            data = None

            path = finders.find(filename)
            if path:
                # Read static files from source (e.g.: the file that's bundled with the
                # Django app that provides it.
                # This also picks up uncollected staticfiles (useful when developing /
                # in DEBUG mode).
                with open(path, "rb") as f:
                    data = f.read()
            else:
                # File was not found by a finder. This commonly happens when running in
                # DEBUG=True with a storage that uses Manifests or alike, since the
                # filename won't match with the source file.
                # In these cases, use the _storage_ to find the file instead:
                with staticfiles_storage.open(filename) as f:
                    data = f.read()

            return {
                "mime_type": mimetypes.guess_type(url)[0],
                "string": data,
            }
    except (ValueError, FileNotFoundError):
        # Looks like this wasn't a staticfile (or maybe it was a missing one?)
        # Let it resolve as a normal URL.
        pass

    try:
        # If the URL is a relative URL, use Django's resolver to figure out how Django
        # would serve this.
        #
        # This should cover all those funky scenarios like:
        # - Custom views that serve dynamically generated files.
        # - Media files (if serving them via Django, which is not recommended).
        if url.startswith("/"):
            view, args, kwargs = resolve(url)
            kwargs["request"] = HttpRequest
            kwargs["request"].method = "GET"
            response = view(*args, **kwargs)

            return {
                "mime_type": mimetypes.guess_type(url)[0],
                "string": response.content,
            }
    except Resolver404 as e:
        raise InvalidRelativeUrl(f"No view matched `{url}`.") from e

    return default_url_fetcher(url)


def render_pdf(
    template: Union[List[str], str],
    file_: IO,
    url_fetcher=django_url_fetcher,
    context: Optional[dict] = None,
):
    """
    Writes the PDF data into ``file_``. Note that ``file_`` can actually be a
    Django Response object as well, since these are file-like objects.

    This function may be used as a helper that can be used to save a PDF file
    to a file (or anything else outside of a request/response cycle).

    :param template: A list of templates, or a single template. If a list of
        templates is passed, these will be searched in order, and the first
        one found will be used.
    :param file: A file-like object (or a Response) where to output
        the rendered PDF.
    :param url_fetcher: See `weasyprint's documentation on url_fetcher`_.
    :param context: Context parameters used when rendering the template.

    .. _weasyprint's documentation on url_fetcher: https://weasyprint.readthedocs.io/en/stable/tutorial.html#url-fetchers
    """  # noqa: E501
    context = context or {}

    if isinstance(template, str):
        template = [template]

    html = select_template(template).render(context)
    HTML(string=html, base_url="not-used://", url_fetcher=url_fetcher,).write_pdf(
        target=file_,
    )
