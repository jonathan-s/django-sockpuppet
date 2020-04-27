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

```bash
# not yet on pypi
pip install django-sockpuppet

# Add these into INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    'channels',
    'sockpuppet'
]

# generates scaffolding for webpack.config.js and installs required js dependencies
# if you prefer to do that manually read the more thorough documentation
python manage.py initial_sockpuppet

# scaffolds a new reflex with everything that's needed.
python manage.py generate_reflex app_name name_of_reflex
```

You're almost there, read about how to tie it all together in the [quickstart documentation][3]

## 💙 Community

- [Discourse](https://stimulus-reflex.discourse.group) - long form async communication
- [Discord](https://discord.gg/XveN625) - We share the discord together with stimulus-reflex, and there is a channel dedicated for python/django discussions.


[1]: https://github.com/hopsoft/stimulus_reflex
[2]: https://youtu.be/Z2DU0qLfPIY?t=670
[3]: #
