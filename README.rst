django-renderpdf
================

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
