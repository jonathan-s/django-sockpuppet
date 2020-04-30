<p align="center">
  <h1 align="center">Welcome to Sockpuppet 👋</h1>
</p>


### 🎉 **You just discovered an exciting new way to build modern, reactive, real-time apps with Django.**

**Why should I spend time exploring this?** If you use current frontend libraries, such as react, vue or angular you end up creating state for the frontend and then updating state changes in the backend through an api.

This means that you forgo server-rendered html with the advantages that brings + you'll end up with a more complex app overall.

With this library you can still use normal django templates, and any frontend state you change will be directly reflected in the backend. Currently this happens through the use of websockets.

This is the django implementation of the excellent rails library [stimulus-reflex][1], which in turn is inspired by [Phoenix LiveView][2].

Hit me up on twitter if you have any questions.  [![Twitter follow](https://img.shields.io/twitter/follow/argparse?style=social)](https://twitter.com/argparse)

## 📚 Documentation

We share the documentation with the excellent stimulusreflex. For the time being the documentation can be found in this [PR](https://github.com/hopsoft/stimulus_reflex/pull/167)

- [Official Documentation](https://docs.stimulusreflex.com)

## ⚡️ Get started

```bash
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


## 🛠 Test things using this repo

```
git clone git@github.com:jonathan-s/django-sockpuppet.git
npm install
npm run build_test
python manage.py runserver
# visit https://localhost:8000/test
```


[1]: https://github.com/hopsoft/stimulus_reflex
[2]: https://youtu.be/Z2DU0qLfPIY?t=670
[3]: #
