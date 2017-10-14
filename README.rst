django-renderpdf
==============

**django-renderpdf** is a Django app to render django templates as PDF files.

Introduction
------------

Rendering PDFs for web developers is generally pretty non-trivial, and there's
no common approach to doing this. django-renderpdf attempts to allow reusing
all the known tools and stills when generating a PDF file in a Django app:

* Use Django template files, which are internally rendered as HTML and them PDF
  files.
* Use staticfiles app to include any CSS or image files.
* Simply subclass a ``PDFView`` class which has an interface very similar to
  Django's own built-in ``View`` classes.

Background
----------

django-renderpdf actually started out as code on multiple of my own projects
(including some public ones).

After some time, it became clear that I'd been copy-pasting PDF-related bits
across different projects, and since co-workers expressed interest in this
design (using the Django templating system to generate PDFs), it finally made
sense to move this into a separate library.

Because of this, documentation is still a work in progress (the code far
outdates this API being public), and while unit tests are lacking, this code
has had ample field testing

Licence
-------

Django-renderpdf is licensed under the ISC licence. See LICENCE for details.

