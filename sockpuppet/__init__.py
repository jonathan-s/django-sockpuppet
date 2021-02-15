import channels

channels_version = channels.__version__.split('.')[0]
if int(channels_version) >= 3:
    from sockpuppet.consumer import SockpuppetConsumerAsgi as SockpuppetConsumer # noqa
else:
    from sockpuppet.consumer import SockpuppetConsumer # noqa

__version__ = '0.5.2'
