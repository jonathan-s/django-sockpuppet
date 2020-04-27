from sockpuppet.reflex import Reflex


class {{ reflex_name|title }}Reflex(Reflex):
    def increment(self, step=1):
        self.count = int(self.element.dataset['count']) + step
