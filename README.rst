django-renderpdf
================

.. image:: https://github.com/WhyNotHugo/django-renderpdf/workflows/Tests/badge.svg
  :target: https://github.com/WhyNotHugo/django-renderpdf/actions/workflows/tests.yml
  :alt: Actions Status

.. image:: https://codecov.io/gh/WhyNotHugo/django-renderpdf/branch/main/graph/badge.svg
  :target: https://codecov.io/gh/WhyNotHugo/django-renderpdf
  :alt: Codecov coverage report

.. image:: https://img.shields.io/pypi/v/django-renderpdf.svg
  :target: https://pypi.python.org/pypi/django-renderpdf
  :alt: Version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/django-renderpdf.svg
  :target: https://pypi.org/project/django-renderpdf/
  :alt: Python versions

.. image:: https://img.shields.io/pypi/l/django-renderpdf.svg
  :target: https://github.com/WhyNotHugo/django-renderpdf/blob/main/LICENCE
  :alt: Licence

**django-renderpdf** is a Django app to render django templates as PDF files.

Introduction
------------

Rendering PDFs for web developers is generally pretty non-trivial, and there's
no common approach to doing this. django-renderpdf attempts to allow reusing
all the known tools and skills when generating a PDF file in a Django app:

* Use Django template files, which are internally rendered as HTML and them PDF
  files.
* Use staticfiles app to include any CSS or image files.
* Simply subclass a ``PDFView`` class which has an interface very similar to
  Django's own built-in ``View`` classes.

Documentation
-------------

The full documentation is available at https://django-renderpdf.readthedocs.io/.

Licence
-------

django-renderpdf is licensed under the ISC licence. See LICENCE for details.
