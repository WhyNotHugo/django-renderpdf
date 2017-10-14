#!/usr/bin/env python3

from setuptools import setup

setup(
    name='django-renderpdf',
    description='A django app to render django templates as PDF files.',
    author='Hugo Osvaldo Barrera',
    author_email='hugo@barrera.io',
    url='https://github.com/WhyNotHugo/django-renderpdf',
    license='ISC',
    packages=['django_renderpdf'],
    include_package_data=True,
    install_requires=[
        'django',
        'weasyprint',
    ],
    long_description=open('README.rst').read(),
    use_scm_version={
        'version_scheme': 'post-release',
        'write_to': 'django_renderpdf/version.py',
    },
    setup_requires=['setuptools_scm'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
