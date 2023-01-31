#!/usr/bin/env python3
from setuptools import setup

with open("README.rst") as f:
    readme = f.read()

setup(
    name="django-renderpdf",
    description="A django app to render django templates as PDF files.",
    author="Hugo Osvaldo Barrera",
    author_email="hugo@barrera.io",
    url="https://django-renderpdf.readthedocs.io/",
    project_urls={
        "GitHub": "https://github.com/WhyNotHugo/django-renderpdf",
        "Funding": "https://github.com/sponsors/WhyNotHugo",
    },
    license="ISC",
    packages=["django_renderpdf"],
    include_package_data=True,
    install_requires=[
        "django>=2.2",
        "weasyprint",
    ],
    extras_require={
        "docs": ["sphinx"],
    },
    long_description=readme,
    use_scm_version={
        "version_scheme": "post-release",
        "write_to": "django_renderpdf/version.py",
    },
    setup_requires=["setuptools_scm"],
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
