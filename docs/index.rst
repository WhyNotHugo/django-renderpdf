.. django_renderpdf documentation master file, created by
   sphinx-quickstart on Thu Sep 24 02:33:13 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-renderpdf
================

**django-renderpdf** is a Django application for generating PDFs via Django.

Our intent is to properly integrate into Django, and have a very simple, yet flexible
API. We follow common Django patterns, so rendering and exposing PDFs is simple.

Index
-----

.. toctree::
   :maxdepth: 2

   index

Installation
------------

You'll first need to install the python package::

   pip install django-renderpdf

You *don't* need to add it to ``INSTALLED_APPS``.

This package depends on ``weasyprint``, which will be installed as a dependency
automatically. However, ``weasyprint`` itself has a few non-Python
dependencies. Make sure the following works before proceeding::

    python -c "import weasyprint"

If the above prints an error, please follow `weasyprint's installation
documentation`_.

.. _`weasyprint's installation documentation`: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation

Usage
-----

As a usage example, lets assume we have to print some shipping labels to dispatch a
product. We'll need to generate a PDF file for this to print.

.. code:: python

    from django.contrib.auth.mixins import LoginRequiredMixin
    from django_renderpdf.views import PDFView

    from myapp import Shipment


    class LabelsView(LoginRequiredMixin, PDFView):
        """Generate labels for some Shipments.

        A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
        """
        template_name = 'my_app/labels.html'

        def get_context_data(self, *args, **kwargs):
            """Pass some extra context to the template."""
            context = super().get_context_data(*args, **kwargs)

            context['shipments'] = Shipment.objects.filter(
                batch_id=kwargs['pk'],
            )

            return context

If anything in the above example seems completely new, I suggest you review the
documentation for Django's `Class-based views`_.

.. _`Class-based views`: https://docs.djangoproject.com/en/3.1/topics/class-based-views/

You still need to include this view in your ``urls.py`` as usual:

.. code:: python

    from django.urls import path

    path(
        '/shipments/labels/<int:pk>/',
        views.LabelsView.as_view(),
        name='shipment_labels',
    )

Now visiting ``/shipments/labels/17``, will return a PDF file which your browser will
render. Note that, since we used the ``LoginRequiredMixin``, anonymous users will be
redirected to the usual login screen, and then back to this view after login.

API
---

PDFView
~~~~~~~

.. autoclass:: django_renderpdf.views.PDFView

Helpers
~~~~~~~

.. autofunction:: django_renderpdf.helpers.render_pdf

.. include:: ../CHANGELOG.rst

Help
----

If you think you found a bug, or need help with something specific:

- Please check existing issues for similar topics.
- If there's nothing relevant, please open a new issue describing your problem, and
  what you've tried so far.

Issues and source code are all in `GitHub <https://www.github.com/WhyNotHugo/django-renderpdf>`_.

Background
----------

django-renderpdf actually started out as code on multiple of my own projects
(including some public ones).

After some time, it became clear that I'd been copy-pasting PDF-related bits
across different projects, and since co-workers expressed interest in this
design (using the Django templating system to generate PDFs), it finally made
sense to move this into a separate library.

Donations
---------

Donations are welcome. See `here <https://github.com/sponsors/WhyNotHugo>`_ for further
details.

Licence
-------

django-renderpdf is licensed under the ISC licence.
