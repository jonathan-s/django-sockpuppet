from unittest.mock import MagicMock

from django.contrib.auth.models import AnonymousUser
from django.urls import resolve

from sockpuppet.consumer import SockpuppetConsumer
from sockpuppet.reflex import Reflex
from sockpuppet.element import Element


def reflex_factory(url, client, user=None, attributes={}, selectors=None, params={}):
    if not user:
        user = AnonymousUser()
    scope = {"session": client.session, "user": user}
    mock_consumer = MagicMock(scope=scope, spec=SockpuppetConsumer)
    element = Element(attributes)
    resolve(url)  # work as an assert that url actually exists
    reflex = Reflex(
        consumer=mock_consumer,
        url=url,
        element=element,
        selectors=selectors,
        params=params,
    )
    return reflex
