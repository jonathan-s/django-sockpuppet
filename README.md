<p align="center">
  <h1 align="center">Welcome to Sockpuppet 👋</h1>
</p>


### 🎉 **You just discovered an exciting new way to build modern, reactive, real-time apps with Django.**

It's a way to avoid fiddling with apis on the backend and then using single page applications on the frontend. Sockpuppet does all the heavylifting for you.

This is the django implementation of the excellent rails library [stimulus-reflex][1], which in turn is inspired by [Phoenix LiveView][2].


## 📚 Documentation

We share the documentation with the excellent stimulusreflex. For the time being the documentation can be found in this [PR](https://github.com/hopsoft/stimulus_reflex/pull/167)

- [Official Documentation](https://docs.stimulusreflex.com)

## ⚡️ Get started

```
    # not yet on pip
    pip install django-sockpuppet
    npm install sockpuppet-js
```

Add it to your `INSTALLED_APPS`:

```
INSTALLED_APPS = (
    ...
    'channels',
    'sockpuppet',
    ...
)
```

Generate an example application to get started

```
python manage.py generate_reflex your_app
```

You're almost there, read about how to tie it all together in the [quickstart documentation][3]

## 💙 Community

- [Discourse](https://stimulus-reflex.discourse.group) - long form async communication
- [Discord](https://discord.gg/XveN625) - We share the discord together with stimulus-reflex, and there is a channel dedicated for python/django discussions.


[1]: https://github.com/hopsoft/stimulus_reflex
[2]: https://youtu.be/Z2DU0qLfPIY?t=670
[3]: #
