# -*- coding: utf-8
import inspect

from django.apps import AppConfig
from django.urls import URLPattern, URLResolver, get_resolver

from .reflex import PROTECTED_VARIABLES, Reflex


class SockpuppetConfig(AppConfig):
    name = 'sockpuppet'

    def ready(self):
        process_resolver(get_resolver())


def get_context_data(self, **context):
    context = self._patched_get_context_data(**context)

    try:
        reflex = self.request.reflex
    except AttributeError:
        pass
    else:
        instance_variables = [
            name for (name, member) in inspect.getmembers(reflex)
            if not name.startswith('__') and name not in PROTECTED_VARIABLES
        ]
        reflex_context = {key: getattr(reflex, key) for key in instance_variables}
        reflex_context['stimulus_reflex'] = True

        reflex.get_context_data(**reflex_context)
        context.update(reflex_context)

    return context


def process_callback(callback):
    try:
        view_class = callback.view_class
        view_class._patched_get_context_data = view_class.get_context_data
        view_class.get_context_data = get_context_data
    except AttributeError:
        pass

    return callback


def process_resolver(resolver: URLResolver) -> None:
    if resolver.callback:
        resolver.callback = process_callback(resolver.callback)

    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLPattern) and pattern.callback:
            pattern.callback = process_callback(pattern.callback)
        elif isinstance(pattern, URLResolver):
            process_resolver(pattern)

    if resolver._populated:
        resolver._populate()
