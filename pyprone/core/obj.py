from pyprone.helpers.type import short_type

class PrObj():
    """
    base calss for Entities, World, Time, Commands
    """
    _obj_count = 0
    def __init__(self, name: str):
        PrObj._obj_count += 1
        self._obj_id = PrObj._obj_count
        self.name = name
        self._tag = short_type(self)
        self.log('created')

    @property
    def tag(self):
        return self._tag

    @property
    def id(self):
        return self._obj_id

    @property
    def whoami(self):
        return f'{self._obj_id:6} | {self.name[0:16]:16} | {self.tag[0:16]:16}'

    def log(self, text: str):
        print(f'{self.whoami} | {str(text)[0:128]}')