<p align="center">
  <h1 align="center">Welcome to Sockpuppet 👋</h1>
</p>


### 🎉 **You just discovered an exciting new way to build modern, reactive, real-time apps with Django.**

It's a way to avoid fiddling with apis on the backend and then using single page applications on the frontend. Sockpuppet does all the heavylifting for you.

This is the django implementation of the excellent rails library [stimulus-reflex][1], which in turn is inspired by [Phoenix LiveView][2].


## 📚 Documentation

- [Official Documentation](https://docs.stimulusreflex.com)

## ⚡️ Get started

```
    # not yet on pip
    pip install django-sockpuppet
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



## Logging in debug mode

An example if you want to enable debug logging for the consumer.

```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG'
    },
    'handlers': {
        'sockpuppet': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'loggers': {
        'sockpuppet': {
            'level': 'DEBUG',
            'handlers': ['sockpuppet']
        }
    }
}
```

[1]: https://github.com/hopsoft/stimulus_reflex
[2]: https://youtu.be/Z2DU0qLfPIY?t=670
[3]: #
