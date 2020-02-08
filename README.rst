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

Prototype status of getting stimulus-reflex to work with Django.

You need to have redis running for this.

.. code-block:: python

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

    visit https://localhost:8000/test

    # in the cli type in python manage.py progressbar in a new window.


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
