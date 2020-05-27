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
            self.text = f'{self.text}'

    @property
    def text(self):
        return self._text

    @property
    def len(self):
        return len(self.text)

    @text.setter
    def text(self, text):
        if len(text) > PrText.cutoff:
            self._text = text[len(text)-PrText.cutoff:len(text)]
        else:
            self._text = text

    # public methods
    def assign(self, text):
        """ assign the whole text """
        self.text = text

    def append(self, text):
        """ append text to the memory """
        if text:
            self.text += f'{text}'
            
    def back(self, blocker='>>>'):
        """ delete the last character """
        if not self.text[self.len-4:self.len] == f'\n{blocker}':
            if self.len > len(blocker):
                self.assign(self.text[0:self.len-1])

    def lastline(self, blocker='>>>') -> str:
        """ return the last line text """
        return self.text[self.text.rfind('\n') + len(blocker) + 1:self.len]

    def clear(self):
        """ clear text memory """
        self.text = ''

def factory(target_obj: any, init_text='') -> PrText:
    """ create PrText from any givn object """
    if isinstance(target_obj, PrText):
        return target_obj
    if isinstance(target_obj, str):
        return PrText(target_obj, init_text)
    return PrText("this is not a PrText Obj")
