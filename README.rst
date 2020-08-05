django-renderpdf
================

.. image:: https://travis-ci.org/WhyNotHugo/django-renderpdf.svg?branch=master
  :target: https://travis-ci.org/WhyNotHugo/django-renderpdf
  :alt: Travis CI build status

.. image:: https://codecov.io/gh/WhyNotHugo/django-renderpdf/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/WhyNotHugo/django-renderpdf
  :alt: Codecov coverage report

.. image:: https://img.shields.io/pypi/v/django-renderpdf.svg
  :target: https://pypi.python.org/pypi/django-renderpdf
  :alt: Version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/django-renderpdf.svg
  :target: https://pypi.org/project/django-renderpdf/
  :alt: Python versions

.. image:: https://img.shields.io/pypi/l/django-renderpdf.svg
  :target: https://github.com/WhyNotHugo/django-renderpdf/blob/master/LICENCE
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
has had ample field testing.

Usage example
-------------

Hint: Though ``PDFView``'s methods has extensive docstrings you should check.

Let's assume we have some ``Shipment`` object, and we want to print PDF labels for it.
Here's a usage code example for a view that does that.

.. code-block:: python

    from django.contrib.auth.mixins import LoginRequiredMixin
    from django_renderpdf.views import PDFView


    class LabelsView(LoginRequiredMixin, PDFView):
        """Generate labels for some Shipments.

        A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
        """
        template_name = 'my_app/labels.html'

        def get_context_data(self, *args, **kwargs):
            """Pass some extra context to the template."""
            context = super().get_context_data(*args, **kwargs)

            context['shipments'] = models.Shipment.objects.filter(
                batch_id=kwargs['pk'],
            )

            return context

And in ``urls.py``:

.. code-block:: python

    from django.urls import path

    path(
        '/shipments/labels/<int:pk>/',
        views.LabelsView.as_view(),
        name='shipment_labels',
    ),

Changelog
---------

v2.0.0
~~~~~~

- Support Python 3.7 and 3.8.
- Support Django 2.2, 3.0 and 3.1.
- Drop support for Django < 2.2.

Licence
-------

django-renderpdf is licensed under the ISC licence. See LICENCE for details.
