from sockpuppet.reflex import Reflex


class ExampleReflex(Reflex):
    def increment(self, step=1):
        self.session['count'] = int(self.element.dataset['count']) + step
