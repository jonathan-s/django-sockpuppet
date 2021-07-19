---
description: >-
  What to keep in mind when safe-guarding your applications.
---

# Authentication

When a reflex is executed you will have access to the underlying session, and as such you will be able to tell whether the user is authenticated or not. Even if the user is not logged it will work as expected.


{% tabs %}
{% tab %}
```python
from sockpuppet.reflex import Reflex

class ExampleReflex(Reflex):
    def check_auth(self):
        user = self.request.user

        if user.is_authenticated:
            # Here you could add a variable that shows that the user is
            # authenticated, or perform other lookups or whatever need be.
        else if user.is_anonymous:
            # Based on this case you could take other measures that changes
            # the context.
```
{% endtab %}
{% endtabs %}

Above you can see an example of what the reflex could look like. Once the `check_auth` method of the reflex method is called from the frontend the template will be updated according to your logic in the reflex.

# Security

If the website uses https, it will be using a secure websocket, another concern when it comes to security are cross-site request forgery (CSRF). You can read more about how this works for [django-channels](https://channels.readthedocs.io/en/stable/topics/security.html).

By default django-sockpuppet is using `AllowedHostsOriginValidator` which means that a websocket can only be opened from the same domains in `ALLOWED_HOSTS`.

In the [setup](https://sockpuppet.argpar.se/setup-django) stage you defined `ASGI_APPLICATION` to `sockpuppet.routing.application`. So if you need to _not_ use the origin validator for any reason you'll need to create a routing file of your own and update the `settings.py` file to reflect that.

If you create your own routing, the only thing to keep in mind is that the javascript expects that the path to the websocket is `/ws/sockpuppet-sync`.
