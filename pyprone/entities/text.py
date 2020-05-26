from pyprone.core import PrObj

class PrText(PrObj):
    """
    entity for text data
    - just a text string memory
    - little bit of helpers(string manipulators)
    """

    cutoff = 102400
    def __init__(self, name: str, init_text=''):
        super().__init__(name)

        self.text = init_text
        if self.text:
            self.text = f'{self.text}\n'

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if len(text) > PrText.cutoff:
            self._text = text[len(text)-PrText.cutoff:len(text)]
        else:
            self._text = text

    # public methods
    def append(self, text):
        """ append text to the memory """
        if text:
            self.text += f'{text}\n'
            self.log(f'append : {text}')

    def clear(self):
        """ clear text memory """
        self.text = ''

def factory(target_obj: any) -> PrText:
    """ create PrText from any givn object """
    if isinstance(target_obj, PrText):
        return target_obj
    if isinstance(target_obj, str):
        return PrText(target_obj)
    return PrText("this is not a PrText Obj")
