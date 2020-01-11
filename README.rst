=============================
Sockpuppet
=============================

.. image:: https://badge.fury.io/py/django-sockpuppet.svg
    :target: https://badge.fury.io/py/django-sockpuppet

.. image:: https://travis-ci.org/jonathan-s/django-sockpuppet.svg?branch=master
    :target: https://travis-ci.org/jonathan-s/django-sockpuppet

.. image:: https://codecov.io/gh/jonathan-s/django-sockpuppet/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jonathan-s/django-sockpuppet

Helping you use websockets in an effective way in views

Documentation
-------------

The full documentation is at https://django-sockpuppet.readthedocs.io.

Quickstart
----------

Install Sockpuppet::

    pip install django-sockpuppet

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'sockpuppet.apps.SockpuppetConfig',
        ...
    )

Add Sockpuppet's URL patterns:

.. code-block:: python

    from sockpuppet import urls as sockpuppet_urls


    urlpatterns = [
        ...
        url(r'^', include(sockpuppet_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
