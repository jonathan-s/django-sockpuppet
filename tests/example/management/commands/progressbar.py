import time
from django.core.management.base import BaseCommand

from sockpuppet.channel import Channel


class Command(BaseCommand):
    help = "Update the progressbar."

    def handle(self, *args, **options):
        channel = Channel('progress')
        status = 0
        while status < 100:
            status += 10
            print(f'Status: {status}')
            channel.set_attribute({
                'selector': "#progress-bar>div",
                'name': "style",
                'value': "width:{status}%".format(status=status)
            })
            channel.broadcast()
            time.sleep(1)  # fake some latency
