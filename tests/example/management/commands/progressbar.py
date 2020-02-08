import time
from django.core.management.base import BaseCommand

from sockpuppet.channel import Channel


class Command(BaseCommand):
    help = "Update the progressbar."

    def handle(self, *args, **options):
        cable_ready = Channel('TestConsumer')
        status = 0
        while status < 100:
            status += 10
            cable_ready.set_attribute({
                'selector': "#progress-bar>div",
                'name': "style",
                'value': "width:{status}%".format(status=status)
            })
            cable_ready.broadcast()
            time.sleep(1)  # fake some latency
