class PrSys():
    def __init__(self, init_text=''):
        self.text = init_text
        if self.text: self.text = f'{self.text}\n'

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
