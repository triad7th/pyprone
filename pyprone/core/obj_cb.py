from .obj import PrObj

class PrObjCb(PrObj):
    """
    callback-able PrObj, bass class of Views
    """
    def __init__(self, name: str):
        super().__init__(name)

    def update(self, **kwargs: dict):
        """please override this method for your need!"""
        if kwargs:
            self.log(kwargs)
        else:
            self.log("update called")
