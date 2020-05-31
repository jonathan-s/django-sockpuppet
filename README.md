<p align="center">
  <h1 align="center">Welcome to Sockpuppet 👋</h1>
  <p align="center">
    <img src="https://img.shields.io/pypi/v/django-sockpuppet"/>
    <img src="https://img.shields.io/npm/v/sockpuppet-js.svg?color=blue" />
    <a href="https://www.npmjs.com/package/sockpuppet-js">
      <img alt="downloads" src="https://img.shields.io/npm/dm/sockpuppet-js.svg?color=blue" target="_blank" />
    </a>
    <a href="https://github.com/jonathan-s/sockpuppet/blob/master/LICENSE">
      <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-brightgreen.svg" target="_blank" />
    </a>
    <a href="https://sockpuppet.argpar.se/" target="_blank">
      <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
    </a>
    <br />
    <a href="#badge">
      <img alt="semantic-release" src="https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg">
    </a>
    <img src="https://travis-ci.org/jonathan-s/django-sockpuppet.svg?branch=master" alt="Tests">
  </p>
</p>


### 🎉 **You just discovered an exciting new way to build modern, reactive, real-time apps with Django.**

**Why should I spend time exploring this?** If you use current frontend libraries, such as react, vue or angular you end up creating state for the frontend and then updating state changes in the backend through an api.

This means that you forgo server-rendered html with the advantages that brings + you'll end up with a more complex app overall.

With this library you can still use normal django templates, and any frontend state you change will be directly reflected in the backend. Currently this happens through the use of websockets.

This is the django implementation of the excellent rails library [stimulus-reflex][1], which in turn is inspired by [Phoenix LiveView][2].

Hit me up on twitter if you have any questions.  [![Twitter follow](https://img.shields.io/twitter/follow/argparse?style=social)](https://twitter.com/argparse)

## 📚 Documentation

- [Official Documentation](https://sockpuppet.argpar.se/)

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


## 🛠 Development in the repo

See some common commands that can be useful for development

```bash
pip install -r requirements_dev.txt
invoke -l
```

Try out a minimal example manually

```
git clone git@github.com:jonathan-s/django-sockpuppet.git
npm install
npm run build_test
python manage.py runserver
# visit https://localhost:8000/test
```

## 🔜 Release

```
pip install -r requirements_dev.txt
invoke release -b feature
```

[1]: https://github.com/hopsoft/stimulus_reflex
[2]: https://youtu.be/Z2DU0qLfPIY?t=670
[3]: https://sockpuppet.argpar.se/quickstart-django
