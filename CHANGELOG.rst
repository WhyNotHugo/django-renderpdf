Changelog
---------

v6.0.0
~~~~~~

- Drop support for Python 3.9 and 3.10.
- Add support for Python 3.14.
- Drop support for Django < 4.2.
- Add support for Django 5.1 and 5.2.
- Require ``weasyprint>=63,<68``.

v5.0.0
~~~~~~

- Fixed documentation not rendering on readthedocs.
- Drop support for Python 3.8.
- Add support for Python 3.11, 3.12 and 3.13.
- Add support for Django 4.1, 4.2 and 5.1.
- Add :ref:`WEASYPRINT_OPTIONS <weasyprint-options>` global setting and
  ``options`` parameter to :func:`~.render_pdf`.

v4.0.0
~~~~~~

- Dropped support for Python 3.6.
- Dropped support for Python 3.7.
- Supported Python versions are now 3.8, 3.9 and 3.10.
- Supported Django versions are now 3.2 and 4.0.

v3.0.1
~~~~~~
- :func:`~.render_pdf` may take a list of templates or a single template. This
  restores compatibility with pre-v3.0.0 interface.

v3.0.0
~~~~~~

- ``get_template_name`` has been deprecated in favour of ``get_template_names``. This
  does not affect usages when ``template_name`` is defined.
- ``get_download_name`` has been deprecated. Override ``download_name`` as a property
  instead.

v2.2.0
~~~~~~

- ``django_renderpdf.views.PDFView.url_fetcher`` is no longer a static method. If you
  were overriding this method, make sure you remove the ``@staticmethod`` decorator
  from your implementation.
- Improved documentation at RTD.

v2.1.0
~~~~~~

- Add handling of relative URLs.
  CSS, image files, and other resources will be resolved using Django's internal URL
  routing. This includes scenarios like serving static or media files via Django, or
  serving thing like custom css via custom Django views.
- Drop support for Python 3.5.

v2.0.1
~~~~~~

- Improve handling of remote ``staticfiles``.

v2.0.0
~~~~~~

- Support Python 3.7 and 3.8.
- Support Django 2.2, 3.0 and 3.1.
- Drop support for Django < 2.2.
