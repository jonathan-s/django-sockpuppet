from sockpuppet.reflex import Reflex


class ExampleReflex(Reflex):
    def increment(self, step=1):
        self.session['count'] = int(self.element.dataset['count']) + step


class DecrementReflex(Reflex):
    def decrement(self, step=1):
        self.session['otherCount'] = int(self.element.dataset['count']) - step
