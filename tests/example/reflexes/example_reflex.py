from sockpuppet.reflex import Reflex


class ExampleReflex(Reflex):
    def increment(self, step=1):
        self.session['count'] = int(self.element.dataset['count']) + step


class DecrementReflex(Reflex):
    def decrement(self, step=1):
        self.session['otherCount'] = int(self.element.dataset['count']) - step


class ParamReflex(Reflex):
    def change_word(self):
        self.word = 'space'


class FormReflex(Reflex):
    def submit(self):
        self.text_output = self.request.POST['text-input']
