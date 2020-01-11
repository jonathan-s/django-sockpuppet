=====
Usage
=====

To use Sockpuppet in a project, add it to your `INSTALLED_APPS`:

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
