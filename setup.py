#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from sockpuppet/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("sockpuppet", "__init__.py")
readme = open('README.md').read()
requirements = open('requirements.txt').readlines()

setup(
    name='django-sockpuppet',
    version=version,
    description="""Helping you use websockets in an effective way in views""",
    long_description=readme,
    author='Jonathan Sundqvist',
    author_email='jonathan@argpar.se',
    url='https://github.com/jonathan-s/django-sockpuppet',
    packages=[
        'sockpuppet',
    ],
    include_package_data=True,
    install_requires=requirements,
    long_description_content_type="text/markdown",
    license="MIT",
    zip_safe=False,
    keywords='django-sockpuppet',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
